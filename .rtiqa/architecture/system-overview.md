# RTIQA System Overview

This document describes the high-level architecture of RTIQA.

## Purpose

The system overview provides an anchor for RTIQA’s technical design. It explains the major subsystems, their responsibilities, and how they interact.

## Core subsystems

### 1. RTIQA App

- Location: `apps/rtiqa_ai/`
- Responsible for RTIQA-specific application logic, DocType definitions, reports, and integrations.
- Uses Frappe hooks and ERPNext extension points.

### 2. Frappe/ERPNext Ecosystem

- Location: external dependency managed by `infra/frappe_docker/`.
- Provides the underlying framework, authentication, and data model.
- RTIQA extends this ecosystem rather than replacing it.

### 3. AI Integration Layer

- Responsible for connecting RTIQA to AI services such as OpenAI and Gemini.
- Handles prompt generation, result validation, and security filtering.
- Must be documented in `docs/09_AI_SYSTEM.md`.

### 4. Infrastructure Reference

- Location: `infra/frappe_docker/` and `docker-compose.yml`.
- Contains local deployment and environment setup guidance.
- Should be treated as infrastructure reference material, not application code.

### 5. Engineering Brain

- Location: `.rtiqa/`
- Holds standards, architecture rules, decision records, and AI engineering artifacts.
- Supports both human and AI contributors in making consistent engineering decisions.

## Data flow

1. User actions are captured through the Frappe UI or API.
2. RTIQA app logic processes requests and updates DocType data.
3. AI integration services are called for AI-enabled features.
4. Results are stored in Frappe-managed data structures and surfaced to users.

## Integration boundaries

- RTIQA logic should remain within `apps/rtiqa_ai/`.
- Infrastructure and deployment references remain in `infra/`.
- AI prompts, standards, and development rules remain in `.rtiqa/`.

## Why this overview exists

A shared system overview keeps RTIQA aligned across contributors. It helps prevent architectural drift and ensures that new work fits the intended project model.
