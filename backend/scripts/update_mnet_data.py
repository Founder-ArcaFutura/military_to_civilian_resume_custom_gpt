from playwright.sync_api import sync_playwright, TimeoutError
import json
import time
import subprocess
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "mnet_data.json"
VERIFIER_PATH = Path(__file__).resolve().parent / "verify_mosids.py"

def get_missing_mosids():
    """Executes the verifier script to get the list of missing MOSIDs."""
    result = subprocess.run(
        ["poetry", "run", "python", str(VERIFIER_PATH)],
        capture_output=True,
        text=True,
        cwd=VERIFIER_PATH.parent.parent,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to run verify_mosids.py: {result.stderr}")

    missing_mosids = []
    for line in result.stdout.strip().split("\n"):
        if line.strip().startswith("-"):
            missing_mosids.append(line.strip().split(" ")[1])
    return missing_mosids

def main():
    missing_mosids = get_missing_mosids()
    if not missing_mosids:
        print("No missing MOSIDs to scrape. The data is already up to date.")
        return

    print(f"Found {len(missing_mosids)} missing MOSIDs. Starting scrape...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            with open(DATA_PATH, "r") as f:
                all_noc_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_noc_data = {}

        # Scrape the full list of MOSIDs from the site to match the text in the dropdown
        page.goto("https://caface-rfacace.forces.gc.ca/mnet-oesc/en/cafSearch")
        all_mosids_on_site = page.locator("#mosidList option").all_inner_texts()
        mosid_map = {m.split(":")[0].strip(): m.strip() for m in all_mosids_on_site if ":" in m}

        for mosid_code in missing_mosids:
            mosid_label = mosid_map.get(mosid_code)
            if not mosid_label:
                print(f"Could not find label for MOSID code {mosid_code}. Skipping.")
                continue

            if mosid_label in all_noc_data:
                print(f"Skipping {mosid_label} (already scraped).")
                continue

            print(f"Scraping data for {mosid_label}...")
            page.goto("https://caface-rfacace.forces.gc.ca/mnet-oesc/en/cafSearch")
            page.wait_for_selector("#mosidList")
            page.select_option("#mosidList", label=mosid_label)
            page.click("#mosidSearch")
            try:
                page.wait_for_selector("#noc_table", timeout=5000)
                noc_data = []
                for row in page.locator("#noc_table tbody tr").all():
                    row.locator("summary").click()
                    page.wait_for_timeout(100) # wait for the page to update
                    noc_code = row.locator("th").inner_text()
                    civilian_title = row.locator("summary > b").inner_text()
                    task_statements = [p.inner_text() for p in row.locator("div#detailPanelBodyTable > p").all()]
                    noc_data.append({
                        "noc_code": noc_code,
                        "civilian_title": civilian_title,
                        "task_statements": task_statements
                    })
                all_noc_data[mosid_label] = noc_data
            except TimeoutError:
                print(f"  > No NOC table found for {mosid_label}. Skipping.")
                all_noc_data[mosid_label] = []

            time.sleep(1) # Be respectful of the server

        with open(DATA_PATH, "w") as f:
            json.dump(all_noc_data, f, indent=4)

        browser.close()
    print("Scraping complete. mnet_data.json has been updated.")

if __name__ == "__main__":
    main()
