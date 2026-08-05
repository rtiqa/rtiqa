# RTIQA Architecture Rules

This document defines the architecture rules for RTIQA. It guides feature development, integration patterns, and system evolution.

## Purpose

RTIQA is built on the Frappe ecosystem. These rules ensure new work fits the platform model and avoids architectural drift.

## Rule set

### 1. Respect module boundaries

Keep feature implementation within `apps/rtiqa_ai/` and use `infra/` only for deployment or infrastructure references. This separation preserves the clarity between application code and environment tooling.

### 2. Prefer extension over modification

Extend Frappe and ERPNext through app hooks, custom DocTypes, and framework extension points. Avoid editing third-party framework source code.

### 3. Keep integrations explicit

Document all external service integrations in `docs/09_AI_SYSTEM.md` or `docs/08_API.md`. Each integration must have a clear purpose, data flow, and security considerations.

### 4. Preserve data ownership and isolation

Design RTIQA multi-tenant behavior so each tenant’s data is isolated and owned by that tenant. Use Frappe’s tenant and site separation patterns when applicable.

### 5. Keep features composable

Build RTIQA features as composable modules. Avoid tightly-coupled implementations that make it hard to extend or replace functionality.

### 6. Document architectural assumptions

Record assumptions and trade-offs in `.rtiqa/decisions/` or `docs/05_ARCHITECTURE.md`. This makes future changes safer and more transparent.

## Why these rules exist

These architecture rules preserve RTIQA’s modularity, make the project safe for contributors, and keep the system aligned with Frappe’s extensibility model.
