"""Tests for the FastAPI HTTP surface."""

from fastapi.testclient import TestClient

from app.mcp_server import app


client = TestClient(app)


def test_get_rank_responsibilities_found():
    response = client.get("/v1/ranks/Captain")
    assert response.status_code == 200
    body = response.json()
    assert body["rank"] == "Captain"
    assert isinstance(body["responsibilities"], list)
    assert body["responsibilities"]


def test_get_rank_responsibilities_not_found():
    response = client.get("/v1/ranks/UnknownRank")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_mosid_profile_found():
    response = client.get("/v1/mosids/00005")
    assert response.status_code == 200
    body = response.json()
    assert body["mosid"] == "00005"
    assert "title" in body
    assert body["equivalencies"]


def test_get_mosid_profile_not_found():
    response = client.get("/v1/mosids/99999")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_batch_lookup_returns_found_entries():
    response = client.post(
        "/v1/mosids:batchLookup",
        json={"mosid_codes": ["00005", "99999"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert "results" in body
    assert "00005" in body["results"]
    assert "99999" not in body["results"]
