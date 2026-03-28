from __future__ import annotations

import json
from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models import FlakeReportRecord


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, report_id: str, report_json: str) -> None:
        self.db.add(FlakeReportRecord(report_id=report_id, report_json=report_json))
        self.db.commit()

    def get(self, report_id: str) -> Optional[dict]:
        rec = self.db.scalar(select(FlakeReportRecord).where(FlakeReportRecord.report_id == report_id))
        return None if not rec else json.loads(rec.report_json)

    def latest(self) -> Optional[dict]:
        rec = self.db.scalar(select(FlakeReportRecord).order_by(desc(FlakeReportRecord.created_at)).limit(1))
        return None if not rec else json.loads(rec.report_json)
