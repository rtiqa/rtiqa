# RTIQA Contribution Rules

This document defines the contribution rules for RTIQA. It ensures contributions are aligned with project priorities and governance.

## Purpose

RTIQA is a community-driven project. These rules clarify contribution expectations and reduce review churn.

## Rule set

### 1. Follow the contributor workflow

Use `CONTRIBUTING.md` and the GitHub issue and PR templates for all contributions. This ensures consistent communication and review readiness.

### 2. Start with an issue for significant work

If a change affects architecture, deployment, or major user flows, open an issue before writing code. This helps align work with RTIQA’s roadmap.

### 3. Keep changes small and focused

Large, sprawling PRs slow review and increase risk. Split big work into incremental, reviewable units.

### 4. Document design decisions

For non-trivial changes, add a brief note to `docs/` or `.rtiqa/decisions/`. This keeps the project history understandable.

### 5. Respect security and privacy

Do not include secrets, credentials, or production data in pull requests, issues, or documentation.

### 6. Use the approved branch strategy

Branch from `develop` for feature work, `main` for hotfixes, and `docs/<name>` for documentation-only work.

## Why these rules exist

Contribution rules keep RTIQA maintainable and transparent. By defining how work should be proposed and reviewed, we reduce friction for both new contributors and maintainers.
