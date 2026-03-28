from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class FlakeItem(BaseModel):
    test_name: str
    file_path: str
    flake_score: float
    fail_rate: float
    rerun_flip_rate: float
    duration_volatility: float
    pattern: str
    recommended_action: str


class FlakeReport(BaseModel):
    report_id: str
    created_at: datetime
    flaky_tests: list[FlakeItem]
    suspicious_files: list[str]
    environment_correlations: list[dict]
    recommendations: list[str]
