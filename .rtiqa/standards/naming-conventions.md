# RTIQA Naming Conventions

This document defines naming conventions for RTIQA code, modules, files, and documentation.
Consistent naming makes the repository easier to navigate and helps AI agents generate predictable artifacts.

## General principles

- Be descriptive and intentional.
- Prefer clarity over brevity.
- Use `RTIQA` as the project prefix only when naming shared or public-facing identifiers.
- Avoid abbreviations except for established project terms such as `RAG` or `API`.

## Python naming

- Modules and files: `snake_case.py`
- Packages: `snake_case`
- Classes: `PascalCase`
- Functions and methods: `snake_case`
- Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

### Module and package examples

- `apps/rtiqa_ai/rtiqa_ai.py`
- `apps/rtiqa_ai/student_profile.py`
- `apps/rtiqa_ai/analytics/report_generator.py`

## Frappe naming

- DocType names: `Title Case` with spaces, e.g. `Student Attendance`.
- DocType modules: `snake_case`, matching the Python module path.
- Doctype field names: `lower_snake_case`.
- Page names: `Title Case`, e.g. `AI Dashboard`.
- Role names: `Title Case`, e.g. `School Administrator`.

## JavaScript and asset naming

- JavaScript/TypeScript files: `kebab-case.js` or `kebab-case.ts` when the file represents a standalone page or component.
- Module files: `snake_case.js` if they map closely to Python modules.
- CSS files: `kebab-case.css`.
- Assets and images: `kebab-case.png`.

## Documentation naming

- Document files: `kebab-case.md` under `docs/`.
- Architecture docs: `kebab-case.md` under `.rtiqa/architecture/`.
- Decision records: numeric prefix followed by `kebab-case`, e.g. `0001-decision-record-format.md`.
- Roadmap items: `kebab-case.md` only when the content is large enough to require separate documentation.

## Configuration and environment names

- Environment variables: `RTIQA_` prefix when custom to this project.
  - Example: `RTIQA_API_KEY`, `RTIQA_SITE_NAME`
- Docker services: `rtiqa-<service>`.
- Compose files: `docker-compose.yml` or `docker-compose.<purpose>.yml`.

## API naming

- REST endpoints: kebab-case nouns, e.g. `/api/v1/student-records`.
- Query parameters: snake_case.
- JSON fields: snake_case.
- GraphQL fields and types: use `camelCase` for fields and `PascalCase` for types when applicable.

## Why these conventions exist

Naming consistency reduces cognitive load and makes RTIQA easier to maintain. It also improves the quality of AI-generated code and documentation by establishing strong, predictable patterns.

## How AI agents should use this document

- Prefer `snake_case` for Python identifiers and file names.
- Prefer `kebab-case` for Markdown, Docker, and public endpoint names.
- Match Frappe naming conventions when generating DocType and UI artifacts.
