from __future__ import annotations


def test_home_and_latest_flow(client) -> None:
    home = client.get("/")
    assert home.status_code == 200

    before = client.get("/api/latest")
    assert before.status_code == 404

    run = client.post("/api/analyze/sample")
    assert run.status_code == 200

    latest = client.get("/api/latest")
    assert latest.status_code == 200
    assert latest.json()["flaky_tests"]
