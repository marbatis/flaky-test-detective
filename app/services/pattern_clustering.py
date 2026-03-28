from __future__ import annotations

import pandas as pd


class PatternClustering:
    def classify(self, scored: pd.DataFrame, raw: pd.DataFrame) -> pd.DataFrame:
        patterns = []
        for _, row in scored.iterrows():
            subset = raw[raw["test_name"] == row["test_name"]]
            env_fail_var = subset.groupby("environment")["pass_fail"].apply(lambda s: (s == "fail").mean())

            if row["rerun_flip_rate"] > 0.35 and row["duration_volatility"] > 0.45:
                pattern = "timing_sensitive"
            elif env_fail_var.max() - env_fail_var.min() > 0.4:
                pattern = "environment_specific"
            elif "network" in str(subset["dependency_tags"].iloc[0]).lower():
                pattern = "network_dependent"
            else:
                pattern = "general_intermittent"
            patterns.append(pattern)

        scored = scored.copy()
        scored["pattern"] = patterns
        return scored
