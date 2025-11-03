"""ETL script to normalize MOSID↔NOC crosswalk tables.

This loader ingests raw tables placed under ``data/raw`` and outputs
normalized CSV and JSON files in ``data/processed`` for downstream
pipelines.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator, Mapping

# Canonical field names and the set of column headers that map to each
FIELD_ALIASES: Mapping[str, tuple[str, ...]] = {
    "mosid": ("mosid", "mos id", "mosid code"),
    "caf_title": ("caf trade title", "caf title", "occupation title"),
    "noc_code": ("noc 2021", "noc", "noc code"),
    "civilian_title": (
        "civilian occupation title",
        "noc title",
        "civilian title",
    ),
    "role_description": ("role description", "summary"),
}

OUTPUT_FIELDS: tuple[str, ...] = (
    "mosid",
    "caf_title",
    "noc_code",
    "civilian_title",
    "role_description",
    "source_file",
    "source_publication_date",
    "transcription_date",
)


@dataclass
class MosidNocRecord:
    """Normalized representation of a MOSID↔NOC mapping."""

    mosid: str
    caf_title: str
    noc_code: str
    civilian_title: str
    role_description: str
    source_file: str
    source_publication_date: str | None = None
    transcription_date: str | None = None

    def to_row(self) -> dict[str, str | None]:
        return {field: getattr(self, field) for field in OUTPUT_FIELDS}


def extract_value(row: Mapping[str, str], aliases: Iterable[str]) -> str | None:
    for alias in aliases:
        if alias in row and row[alias]:
            return row[alias].strip()
    return None


def normalize_headers(row: Mapping[str, str]) -> dict[str, str]:
    return {key.strip().lower(): value for key, value in row.items() if key}


def sanitize_noc_code(raw: str | None) -> str:
    if not raw:
        return ""
    cleaned = "".join(ch for ch in raw if ch.isalnum())
    return cleaned or raw.strip()


def iter_raw_rows(raw_path: Path) -> Iterator[tuple[str, dict[str, str]]]:
    for file_path in sorted(raw_path.glob("**/*")):
        if file_path.suffix.lower() not in {".csv", ".tsv"}:
            continue
        with file_path.open(newline="", encoding="utf-8-sig") as handle:
            sample = handle.read(2048)
            handle.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
            except csv.Error:
                dialect = csv.excel
            reader = csv.DictReader(handle, dialect=dialect)
            for row in reader:
                yield (file_path.name, normalize_headers(row))


def derive_metadata(filename: str) -> tuple[str | None, str | None]:
    """Best-effort metadata extraction from file naming conventions."""
    stem = Path(filename).stem
    parts = stem.split("_")
    publication = None
    transcription = None
    for part in parts:
        if part.isdigit() and len(part) == 8:
            publication = f"{part[:4]}-{part[4:6]}-{part[6:]}"
        elif part.isdigit() and len(part) == 4:
            publication = part
    transcription = datetime.now(timezone.utc).date().isoformat()
    return publication, transcription


def build_record(filename: str, row: Mapping[str, str]) -> MosidNocRecord | None:
    values = {}
    for field, aliases in FIELD_ALIASES.items():
        value = extract_value(row, aliases)
        if value:
            if field == "noc_code":
                value = sanitize_noc_code(value)
            values[field] = value
    mosid = values.get("mosid", "").strip()
    noc_code = values.get("noc_code", "").strip()
    if not mosid or not noc_code:
        return None
    caf_title = values.get("caf_title", "").strip()
    civilian_title = values.get("civilian_title", "").strip()
    role_description = values.get("role_description", "").strip()
    publication, transcription = derive_metadata(filename)
    return MosidNocRecord(
        mosid=mosid,
        caf_title=caf_title,
        noc_code=noc_code,
        civilian_title=civilian_title,
        role_description=role_description,
        source_file=filename,
        source_publication_date=publication,
        transcription_date=transcription,
    )


def dedupe_records(records: Iterable[MosidNocRecord]) -> list[MosidNocRecord]:
    seen: dict[tuple[str, str], MosidNocRecord] = {}
    for record in records:
        key = (record.mosid, record.noc_code)
        seen[key] = record
    return list(seen.values())


def write_csv(records: Iterable[MosidNocRecord], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_row())


def write_json(records: Iterable[MosidNocRecord], path: Path) -> None:
    serializable = [asdict(record) for record in records]
    with path.open("w", encoding="utf-8") as handle:
        json.dump(serializable, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def ingest(raw_dir: Path, output_dir: Path) -> list[MosidNocRecord]:
    output_dir.mkdir(parents=True, exist_ok=True)
    records = [
        record
        for filename, row in iter_raw_rows(raw_dir)
        if (record := build_record(filename, row)) is not None
    ]
    normalized = dedupe_records(records)
    normalized.sort(key=lambda rec: (rec.mosid, rec.noc_code))
    write_csv(normalized, output_dir / "mosid_noc.csv")
    write_json(normalized, output_dir / "mosid_noc.json")
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize MOSID↔NOC crosswalk tables.")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "data" / "raw",
        help="Directory containing raw MOSID↔NOC tables",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "data" / "processed",
        help="Directory for normalized outputs",
    )
    args = parser.parse_args()

    ingest(args.raw_dir, args.output_dir)


if __name__ == "__main__":
    main()
