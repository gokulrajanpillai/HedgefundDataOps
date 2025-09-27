# Hedge Fund Data Reliability Platform (DataOps MVP)

> **One-liner:** A Python + CI/CD + monitoring framework that guarantees clean, validated, auditable market & alternative data—ready for quants and trading models.

---

## Why this exists (current market pain)

* **Schema drift & silent failures** corrupt downstream signals.
* **Data latency** (late/partial drops) causes missed opportunities and bad fills.
* **Fragmented scripts** across teams; no single, tested path to production.
* **No lineage/audit trail** to satisfy SEC/FCA reviews and internal model risk.
* **Slow vendor onboarding** (each new data feed = bespoke work + high MTTR on breakage).
* **Cloud cost sprawl** from long‑running jobs and zombie resources.
* **No SLOs** for data quality/arrival → ops discovers issues after quants do.

---

## What this project delivers (product pillars)

1. **Multi‑source ingestion (batch + streaming)**

   * Market data + fundamentals + alt‑data; plug‑in connectors.
2. **Data contracts & validation**

   * Pydantic schemas + CI checks; fail fast, isolate bad rows, never pollute stores.
3. **CI/CD for data pipelines**

   * Tests on every PR; reproducible builds with Docker; infra as code with Terraform.
4. **Lineage & auditability**

   * Metadata records for each run: source, schema version, rows ingested, rejects, checksum.
5. **Quant‑ready outputs**

   * Normalized Parquet for notebooks; Snowflake/Postgres tables for models & dashboards.
6. **Observability & alerting**

   * Prometheus metrics + Grafana dashboards; Slack/Teams daily quality reports.
7. **Cost guardrails**

   * Tags, budgets, autoscaling; kill‑switch jobs for idle/oversized compute.

> **Outcome:** Clean, timely, compliant data—**every day without fail**—so quants build alpha instead of cleaning pipelines.

---

## Who it’s for

* Heads of Data / CTO / CDO
* Quant leads & platform teams
* Risk/compliance stakeholders who need audit‑ready data movement

---

## MVP architecture (high level)

                ┌─────────────────────────┐
                │  Market & Alt Data APIs │
                │ (Yahoo Finance + mocks) │
                └───────────────┬─────────┘
                                │
                        [Ingestion Layer]
                                │
             ┌──────────────────┴──────────────────┐
             │                                     │
       [Validation]                          [Audit Logs]
 (Pydantic schema checks)            (Errors, metadata, lineage)
             │                                     │
             └──────────► [Storage Layer] ◄────────┘
                       (Postgres + Parquet)

                                │
                        [Observability Layer]
                                │
                    ┌───────────┴───────────┐
                    │                       │
             Grafana Dashboards       Slack/Teams Alerts



```
[Data Vendors]
  |  (Bloomberg/Refinitiv mocks, Yahoo Finance, Alt‑data APIs)
  v
[Ingestion Orchestrator]
  Airflow/Prefect → Python requests/async → backoff/retry → idempotent writes
  v
[Validation]
  Pydantic data contracts → row/field quarantine → run metrics
  v
[Transform]
  Pandas (MVP) / PySpark (scale) → normalized domain tables
  v
[Storage]
  Parquet (lake) + Snowflake/Postgres (warehouse)
  |\
  | \__ [Lineage & Audit]
  |       Run metadata (job_id, src, schema_ver, checksums, rejects)
  |
  \__ [Serving/API]
       FastAPI endpoints for on‑demand pulls (optional)

[Observability]
  Prometheus exporters → Grafana dashboards → Slack/Teams alerts
```



---

## Key design principles

* **Fail‑fast, never dirty**: reject/isolated bad data; do not propagate.
* **Idempotent & replayable**: safe to re‑run; deterministic outputs.
* **Observable by default**: emit metrics/logs/events for every stage.
* **Compliance‑ready**: immutable audit logs + data lineage.
* **Vendor‑agnostic**: no lock‑in; connectors are swappable.
* **Security‑first**: least‑privilege IAM; secrets in vaults (not in repo).

---

## Repo scope (MVP)

* `etl/` – ingestion, transform, validation (Python)
* `dags/` – Airflow/Prefect orchestration
* `tests/` – schema & integration tests (CI)
* `infra/` – Dockerfile, docker‑compose; Terraform stubs
* `monitoring/` – Grafana dashboard JSON; Prometheus rules
* `.github/workflows/` – CI pipeline

> **Status:** MVP scaffold with one live feed (Yahoo Finance) + one alt‑data mock; designed to extend to institutional feeds.

---

## Roadmap

* **v0.1 (MVP):** Single‑feed ingestion; schema validation; CI; basic Grafana; daily Slack report.
* **v0.2:** Multi‑feed connectors; partitioned Parquet; lineage DB; API for ad‑hoc pulls.
* **v0.3:** Streaming (WebSocket/Kafka); drift detection; cost policies as code (OPA).
* **v1.0:** Snowflake integration; RBAC; compliance reports; SLOs & error budgets.

---

## Business outcomes (what stakeholders get)

* **Time‑to‑alpha:** Quants get clean datasets Day 1; new feeds onboarded in days, not weeks.
* **Risk reduction:** Zero bad‑data trades; audit trails for regulators.
* **Cost control:** Autoscaling + guardrails to keep cloud spend predictable.

---

## Quickstart (local)

1. Ensure **Python 3.11** and **Docker** are installed.
2. Clone & enter: `git clone <your-repo-url> && cd hedgefund-dataops`
3. (Soon) `docker compose up -d` to boot Airflow + Grafana (MVP stack).
4. `pip install -r requirements.txt` and run `python etl/ingestion.py` to fetch a sample batch.

> Detailed setup, credentials management, and cloud deployment docs will live in `/docs`.

---

## Security & compliance notes

* No secrets in source control; use `.env` (gitignored) or a secrets manager.
* Emit immutable run logs to a dedicated audit store.
* Enforce code review + CI checks on every pipeline change.

---

## License

TBD (default: proprietary / all rights reserved for client deployments).

## Maintainers

Core engineering: DevOps & Data Platform team.

---

## Developer Setup
For detailed instructions on setting up your development environment (virtualenv, dependencies, API keys, and running the pipeline), see [docs/DEVELOPER_SETUP.md](docs/DEVELOPER_SETUP.md).
