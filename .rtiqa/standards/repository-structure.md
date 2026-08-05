# RTIQA Repository Structure

This document describes the canonical repository structure for RTIQA. It is the reference for where engineers should place new code, docs, and infrastructure artifacts.

## Top-level layout

- `apps/` — RTIQA application code; the primary app currently lives in `apps/rtiqa_ai/`.
- `config/` — repository-specific configuration and environment templates.
- `docker/` — Docker build artifacts and helper assets.
- `docs/` — public project documentation.
- `infra/` — infrastructure support and deployment references. Current Frappe tooling lives under `infra/frappe_docker/`.
- `.rtiqa/` — RTIQA engineering system foundation.
- `.devcontainer/` — development container configuration.
- `docker-compose.yml` — local environment reference.
- `pyproject.toml` — Python tooling and build configuration.
- `README.md` — project introduction and onboarding guidance.
- `LICENSE` — project license terms.

## `apps/`

- Primary location for RTIQA application modules.
- New RTIQA features and customizations should be added under `apps/rtiqa_ai/`.
- Avoid adding unrelated or experimental application code outside this folder.

## `docs/`

- Use this directory for public-facing project documentation.
- Place high-level guides, architecture docs, roadmap material, and contributor information here.
- Keep each document focused and link to related documents rather than duplicating large content.

## `infra/`

- Store deployment and environment reference code here.
- `infra/frappe_docker/` is used for Frappe deployment support and should remain clearly separated from RTIQA application code.
- Use `infra/` for external infrastructure modules, not for RTIQA application logic.

## `.rtiqa/`

- This directory is the engineering brain for RTIQA.
- Add standards, rules, architecture references, decisions, and AI engineering artifacts here.
- Do not place executable application code in `.rtiqa/`.

## Naming and boundaries

- Keep core application code in `apps/rtiqa_ai/`.
- Keep platform-specific infrastructure and deployment code in `infra/`.
- Keep documentation and governance in top-level `docs/` and `.rtiqa/`.

## Versioning and releases

- `main` is the stable branch.
- `develop` is the integration branch.
- Release branches should be named `release/<version>`.
- Tag releases with semantic version numbers.

## Why this structure exists

A clean repository structure allows RTIQA to scale without becoming fragmented. It separates application code from infrastructure, documentation, and engineering governance, making it easier for humans and AI agents to find the correct source of truth.

## AI agent guidance

- Use `.rtiqa/` for engineering rules, standards, and architecture guidance.
- Use `docs/` for public-facing, user-oriented documentation.
- Use `apps/rtiqa_ai/` for application code generation only when the AI task explicitly targets RTIQA features.
- Do not generate or modify files under `infra/frappe_docker/` unless the task is infrastructure-specific and authorized.
