from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.analysis_service import AnalysisService

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


def get_service(db: Session = Depends(get_db)) -> AnalysisService:
    return AnalysisService(db)


@router.get("/", response_class=HTMLResponse)
def home(request: Request, service: AnalysisService = Depends(get_service)) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html", context={"report": service.latest()})


@router.post("/run", response_class=HTMLResponse)
def run(request: Request, service: AnalysisService = Depends(get_service)) -> HTMLResponse:
    report = service.analyze()
    return templates.TemplateResponse(request=request, name="index.html", context={"report": report})
