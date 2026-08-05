# RTIQA Dependency Policy

This document defines the dependency policy for RTIQA. It explains how dependencies should be selected, managed, and reviewed.

## Purpose

Dependencies shape RTIQA’s security posture, maintainability, and deployment complexity. A disciplined policy keeps the project stable and auditable.

## Policy

### 1. Prefer native Frappe/ERPNext capabilities

Before adding a new dependency, verify whether the required functionality can be implemented using Frappe or ERPNext built-in features.

### 2. Use dependencies only when necessary

- Add dependencies only for capabilities that are difficult to implement safely or efficiently in-house.
- Prefer lightweight libraries with strong maintenance records.

### 3. Document all new dependencies

- Document new dependencies in `docs/05_ARCHITECTURE.md` or `.rtiqa/architecture/system-overview.md`.
- Record why the dependency is needed and any risks it introduces.

### 4. Review dependency licences

- Ensure dependency licenses are compatible with RTIQA’s project license.
- Do not introduce dependencies with restrictive or commercial-only licenses without explicit approval.

### 5. Manage dependency updates

- Update dependencies proactively for security and compatibility.
- Test updates against RTIQA app behavior before merging.

### 6. Avoid unnecessary dependency proliferation

- Reuse existing dependencies rather than adding new ones for similar capabilities.
- Consolidate shared utilities within RTIQA when it is safer than adding a new external package.

## Why this policy exists

Dependencies are a major source of risk in open-source projects. This policy ensures RTIQA remains maintainable, secure, and compatible with the Frappe ecosystem.

## AI agent guidance

- When generating code, prefer dependencies already present in the repository or the Frappe ecosystem.
- Do not introduce new package dependencies without a documented justification.
- Use this policy to evaluate whether a dependency addition is warranted.
