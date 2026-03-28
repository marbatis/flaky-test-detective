from __future__ import annotations

from app.services.data_loader import DataLoader
from app.services.flake_scoring import FlakeScoring
from app.services.pattern_clustering import PatternClustering


def test_clustering_output_shape() -> None:
    raw = DataLoader().load()
    scored = FlakeScoring().score(raw)
    clustered = PatternClustering().classify(scored, raw)
    assert "pattern" in clustered.columns
    assert clustered["pattern"].notna().all()
