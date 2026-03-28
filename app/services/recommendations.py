from __future__ import annotations

import pandas as pd


class RecommendationEngine:
    ACTION_MAP = {
        "timing_sensitive": "rewrite",
        "environment_specific": "investigate dependency",
        "network_dependent": "quarantine",
        "general_intermittent": "instrument",
    }

    def attach_actions(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["recommended_action"] = df["pattern"].map(self.ACTION_MAP).fillna("monitor only")
        return df

    def summary_recommendations(self, df: pd.DataFrame) -> list[str]:
        top = df.head(5)
        recs = []
        for _, row in top.iterrows():
            recs.append(f"{row['test_name']}: {row['recommended_action']}")
        return recs
