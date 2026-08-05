# RTIQA Module Boundaries

This document defines the module boundaries for RTIQA. It clarifies where functionality should live and how modules should interact.

## Purpose

Clear module boundaries prevent code from becoming tightly coupled and make RTIQA easier to extend and maintain.

## Boundary definitions

### `apps/rtiqa_ai/`

- Primary location for RTIQA application modules.
- Contains custom DocTypes, business logic, API endpoints, reports, and feature modules.
- New RTIQA functionality should be implemented here.

### `infra/frappe_docker/`

- Infrastructure and deployment support for Frappe and RTIQA.
- Contains environment definitions, container orchestration references, and deployment tools.
- Do not place application or business logic here.

### `docs/`

- Public and community-facing documentation.
- Contains user-facing architecture, roadmap, setup, and contribution documentation.

### `.rtiqa/`

- Engineering brain for RTIQA.
- Contains standards, rules, architecture references, decisions, and AI workflow artifacts.
- Use this space for engineering governance and not for application logic.

## Interaction rules

- Cross-module dependencies should be explicit and minimal.
- `apps/rtiqa_ai/` may depend on `infra/frappe_docker/` only for deployment-related configuration references.
- Documentation may reference code and architecture artifacts, but should not duplicate implementation details.
- `.rtiqa/` may reference any repository artifact for governance and engineering guidance.

## Why these boundaries exist

Well-defined boundaries keep the repository organized and prevent unrelated concerns from mixing. This reduces review complexity and makes it easier for AI agents to infer the correct location for new content.
