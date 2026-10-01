# Veles test strategy

The suite is split by execution contract rather than only by file location.

## Deterministic tests

```bash
pytest -m unit
pytest -m integration
pytest -m e2e
```

- `unit`: one domain module; no network.
- `integration`: several modules using saved fixtures or mocks; no network.
- `e2e`: full report-output contracts and delivery reconciliation.

## Optional live-provider tests

Live external calls are opt-in:

```bash
pytest --run-live -m live_provider
```

Tests marked `live_provider` are skipped by default. Unit, integration, and end-to-end tests must not depend on Yahoo Finance, OpenAI, SEC availability, or current market data.

## Provider fixtures

Stable provider payloads live under `tests/fixtures/providers/`. Add a small, de-identified fixture when a provider response shape or normalization edge case needs coverage.

## Semantic snapshots

JSON contract snapshots live under `tests/snapshots/`. Snapshot prepared report data rather than PDF bytes, timestamps, image files, or layout coordinates. This catches financial and report-contract regressions without creating fragile tests.

## Delivery reconciliation

`services.reports.reconciliation.validate_report_for_delivery()` compares structured dashboard, valuation, executive-summary metric blocks, and chart manifests against the canonical `financial_render_model`.

The report service uses this as a fail-closed delivery gate. A report with contradictory values or leaked unsafe metrics is rejected before delivery.
