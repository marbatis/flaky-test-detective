from __future__ import annotations

from app.services.data_loader import DataLoader
from app.services.flake_scoring import FlakeScoring


def test_flake_score_computation() -> None:
    df = DataLoader().load()
    scored = FlakeScoring().score(df)
    assert not scored.empty
    assert scored["flake_score"].max() > scored["flake_score"].min()


def test_dataset_has_expected_patterns() -> None:
    df = DataLoader().load()
    assert "test_api_network_retry" in set(df["test_name"])
    assert "windows" in set(df["environment"])
