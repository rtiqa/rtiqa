# RTIQA AI Development Rules

This document defines the rules for AI-assisted development in RTIQA.

## Purpose

RTIQA embraces AI-assisted engineering while maintaining human oversight and project integrity. These rules ensure AI outputs are consistent, secure, and aligned with RTIQA architecture.

## Scope

- AI-generated code and documentation
- AI-assisted reviews and design proposals
- AI agents operating on the RTIQA repository

## Rule set

### 1. Use AI as a tool, not a substitute

AI may assist with code generation, documentation drafts, and design suggestions. Human maintainers must review and approve all AI-generated content.

### 2. Follow RTIQA standards

AI-generated outputs must follow `.rtiqa/standards/coding-standards.md`, `.rtiqa/standards/naming-conventions.md`, and `.rtiqa/standards/documentation-standards.md`.

### 3. Avoid unauthorized modifications

AI agents must not modify Frappe core files or `infra/frappe_docker/` without explicit maintainer approval.

### 4. Verify architecture boundaries

AI-generated changes must respect the module boundaries defined in `.rtiqa/architecture/module-boundaries.md` and the repository structure.

### 5. Annotate AI contributions

When AI generates content, include a short note in the commit or PR description that identifies the assisted source and the validation steps taken.

### 6. Do not invent unsupported features

AI should not introduce features, integrations, or workflows that are not explicitly requested or documented in RTIQA planning artifacts.

## Why these rules exist

AI can accelerate RTIQA development, but uncontrolled generation introduces risk. These rules preserve quality, maintainability, and the project’s long-term architecture.
