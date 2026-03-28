# Task Environment

## 1. Rational objective
Identify likely flaky tests from synthetic CI history and provide deterministic remediation recommendations.

## 2. PEAS
- Performance: rank flaky tests, classify failure patterns, provide actionable recommendations.
- Environment: synthetic CI/test history.
- Actuators: API and web reports.
- Sensors: pass/fail history, reruns, durations, environment and dependency tags.

## 3. Environmental dimensions
Noisy and partially observable test signals, environment variability, intermittent failures.

## 4. Problem formalization
Compute a flake score from fail rate, rerun inconsistency, and duration volatility, then classify and recommend action.

## 5. Architecture choice
Data loader + deterministic scoring + heuristic clustering + recommendations.

## 6. Guardrails / workflow maturity
No auto-muting tests in CI; output is decision support only.
