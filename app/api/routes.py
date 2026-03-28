from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.models import FlakeReport
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api", tags=["api"])


def get_service(db: Session = Depends(get_db)) -> AnalysisService:
    return AnalysisService(db)


@router.post("/analyze/sample", response_model=FlakeReport)
def analyze_sample(service: AnalysisService = Depends(get_service)) -> FlakeReport:
    return service.analyze()


@router.get("/latest", response_model=FlakeReport)
def latest(service: AnalysisService = Depends(get_service)) -> FlakeReport:
    report = service.latest()
    if not report:
        raise HTTPException(status_code=404, detail="No report yet")
    return report
