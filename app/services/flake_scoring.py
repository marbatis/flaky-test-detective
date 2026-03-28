from __future__ import annotations

import pandas as pd


class FlakeScoring:
    def score(self, df: pd.DataFrame) -> pd.DataFrame:
        grouped = df.groupby(["test_name", "file_path"], as_index=False)
        rows = []

        for (test_name, file_path), g in grouped:
            fail_rate = (g["pass_fail"] == "fail").mean()
            rerun_flip_rate = (
                ((g["pass_fail"] != g["rerun_result"]) & g["rerun_result"].isin(["pass", "fail"])).mean()
            )
            duration_volatility = g["duration"].std(ddof=0) / max(g["duration"].mean(), 1e-6)

            score = min(100.0, 45 * fail_rate + 35 * rerun_flip_rate + 20 * duration_volatility)

            rows.append(
                {
                    "test_name": test_name,
                    "file_path": file_path,
                    "fail_rate": round(float(fail_rate), 3),
                    "rerun_flip_rate": round(float(rerun_flip_rate), 3),
                    "duration_volatility": round(float(duration_volatility), 3),
                    "flake_score": round(float(score), 2),
                }
            )

        out = pd.DataFrame(rows).sort_values("flake_score", ascending=False)
        return out
