from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.repositories.report_repo import ReportRepository
from app.schemas.models import FlakeItem, FlakeReport
from app.services.data_loader import DataLoader
from app.services.flake_scoring import FlakeScoring
from app.services.pattern_clustering import PatternClustering
from app.services.recommendations import RecommendationEngine


class AnalysisService:
    def __init__(self, db: Session):
        self.repo = ReportRepository(db)
        self.loader = DataLoader()
        self.scorer = FlakeScoring()
        self.cluster = PatternClustering()
        self.reco = RecommendationEngine()

    def analyze(self) -> FlakeReport:
        raw = self.loader.load()
        scored = self.scorer.score(raw)
        clustered = self.cluster.classify(scored, raw)
        final = self.reco.attach_actions(clustered)

        items = [FlakeItem(**row) for row in final.head(20).to_dict(orient="records")]
        suspicious_files = final.groupby("file_path")["flake_score"].mean().sort_values(ascending=False).head(5)
        env_corr = (
            raw.groupby(["environment", "pass_fail"]).size().reset_index(name="count").to_dict(orient="records")
        )

        report = FlakeReport(
            report_id=str(uuid4()),
            created_at=datetime.now(timezone.utc),
            flaky_tests=items,
            suspicious_files=suspicious_files.index.tolist(),
            environment_correlations=env_corr,
            recommendations=self.reco.summary_recommendations(final),
        )

        self.repo.save(report.report_id, json.dumps(report.model_dump(mode="json"), default=str))
        return report

    def latest(self) -> Optional[FlakeReport]:
        raw = self.repo.latest()
        if not raw:
            return None
        return FlakeReport.model_validate(raw)
