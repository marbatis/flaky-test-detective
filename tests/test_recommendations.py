from __future__ import annotations

from app.services.recommendations import RecommendationEngine


def test_recommendation_generation(client) -> None:
    response = client.post("/api/analyze/sample")
    assert response.status_code == 200
    body = response.json()
    assert body["recommendations"]


def test_recommendation_logic_maps_patterns() -> None:
    import pandas as pd

    df = pd.DataFrame({"pattern": ["network_dependent", "timing_sensitive"]})
    out = RecommendationEngine().attach_actions(df)
    assert set(out["recommended_action"]) == {"quarantine", "rewrite"}
