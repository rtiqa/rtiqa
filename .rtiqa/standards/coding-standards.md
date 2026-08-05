# RTIQA Coding Standards

This document defines the coding standards for RTIQA. It applies to all code produced by humans and AI agents within this repository.

## Purpose

RTIQA is built on the Frappe ecosystem and uses Python and JavaScript for application and integration logic. These standards ensure consistent style, reliable behavior, and low maintenance costs.

## Python Standards

### Formatting

- Use `black` for all Python formatting.
- Configure `black` with `line-length = 88` where applicable.
- Do not manually reformat code that is already formatted by `black`.

### Linting

- Use `ruff` for static analysis and linting.
- Enforce the selected rule set in `pyproject.toml`.
- Fix all `E`, `F`, `I`, `UP`, and `B` violations before review.

### Typing

- Use type annotations for public functions and methods.
- Prefer `typing.Annotated` for metadata when relevant.
- Avoid overly broad types like `Any` unless a clear justification exists.

### Code layout

- Keep functions short and focused on a single responsibility.
- Prefer composition over deep inheritance.
- Keep modules under 200 lines when possible.
- Use meaningful names for variables, functions, and classes.

### Frappe-specific conventions

- Place RTIQA app code inside `apps/rtiqa_ai/`.
- Use Frappe hooks and extension points; do not modify Frappe core.
- Document custom DocTypes, pages, reports, and API endpoints in `docs/`.
- Keep business logic in Python modules and use client scripts only for UI interactions.

### Testing

- Every new feature or fix must include a regression test.
- Use `pytest` conventions and place tests close to the code they validate.
- Write tests that verify behavior, not implementation details.

## JavaScript / TypeScript Standards

### Formatting

- Use `prettier` if the project includes JavaScript or TypeScript sources.
- Align with the existing style used in Frappe front-end extensions.

### Linting

- Apply `eslint` for new JavaScript/TypeScript work.
- Enforce code quality rules in the project configuration.
- Favor typed interfaces or JSDoc for public API contracts.

### Best practices

- Keep UI logic decoupled from business rules.
- Use module imports rather than global script dependencies.
- Avoid inline script blocks for new work.

## SQL and Database Patterns

- Use Frappe ORM operations where possible.
- Avoid raw SQL unless required for performance or capabilities not exposed by the framework.
- Parameterize queries to prevent SQL injection.
- Document any custom query or schema change in `docs/`.

## Infrastructure and Configuration

- Keep infrastructure code declarative and version-controlled.
- Use `docker-compose.yml` and `infra/frappe_docker/` for local environment references.
- Do not hard-code secrets or credentials in source files.

## Code Review Checklist

- Does the code follow these coding standards?
- Is the implementation aligned with RTIQA architecture and module boundaries?
- Are tests included and passing?
- Is the change documented appropriately?
- Does the change avoid modifying Frappe core or third-party vendor files?

## Why these standards exist

Consistent standards reduce review friction and encourage high-quality contributions. RTIQA uses Frappe and AI-driven development, so a clear and specific coding standard helps both human and machine contributors deliver predictable results.
