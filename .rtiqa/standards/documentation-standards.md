# RTIQA Documentation Standards

This document explains how to write and maintain RTIQA documentation.

## Purpose

RTIQA documentation is the single source of truth for project strategy, design, and contribution practices. These standards ensure documentation is accurate, specific, and useful.

## Documentation types

- Public product and architecture docs: `docs/`
- Engineering system docs: `.rtiqa/`
- Issue templates: `.github/ISSUE_TEMPLATE/`
- PR templates: `.github/PULL_REQUEST_TEMPLATE.md`
- Decision records: `.rtiqa/decisions/`

## Writing style

- Use active voice.
- Prefer concrete examples over abstract descriptions.
- Be specific to RTIQA; avoid generic statements.
- Keep sections short and use headings to organize content.
- Use `RTIQA` as the project name consistently.

## Document structure

Each document should include:

1. Purpose: why this document exists.
2. Scope: what it covers and what it does not cover.
3. Guidance: practical instructions or rules.
4. References: links to related documents.

## Naming and format

- Use `kebab-case.md` for documentation file names.
- Prefer `##` headings for major sections and `###` for subsections.
- Use code fences for examples, configuration snippets, and commands.
- Avoid overly long paragraphs.

## Maintenance

- Update documentation whenever behavior, architecture, or process changes.
- Link new docs from `README.md` and relevant index pages.
- Remove stale or duplicated content rather than leaving outdated docs in place.

## Review

- All documentation changes should be reviewed for accuracy.
- Validate that examples match current repository structure and tools.
- Prefer factual guidance over aspirational language.

## Why this standard exists

RTIQA is an engineering-driven open-source project. Good documentation prevents misunderstandings, accelerates onboarding, and makes AI-assisted workflows reliable.

## AI agent guidance

- Generate documentation only when the content can be made specific to RTIQA.
- Reference existing RTIQA standards and architecture documents.
- Do not invent unspecified features or workflows.
