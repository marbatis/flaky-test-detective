from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


class DataLoader:
    def __init__(self, dataset_path: Optional[Path] = None):
        root = Path(__file__).resolve().parents[2]
        self.dataset_path = dataset_path or (root / "data" / "ci_history.csv")

    def load(self) -> pd.DataFrame:
        df = pd.read_csv(self.dataset_path)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
