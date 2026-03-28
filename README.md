# flaky-test-detective

Deterministic analyzer for synthetic CI history to rank flaky tests, detect suspicious patterns, and recommend remediation actions.

## MVP Features
- Flake score per test using:
  - fail rate
  - rerun inconsistency
  - duration volatility
- Pattern classification:
  - timing_sensitive
  - environment_specific
  - network_dependent
  - general_intermittent
- Recommended actions:
  - quarantine
  - rewrite
  - instrument
  - investigate dependency
  - monitor only
- API + web report

## Local Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Routes
- `GET /`
- `POST /run`
- `POST /api/analyze/sample`
- `GET /api/latest`

## Heroku
Includes `Procfile`, `runtime.txt`, `.env.example`, and GitHub Actions workflow.
