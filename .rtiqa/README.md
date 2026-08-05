# .rtiqa Engineering System

The `.rtiqa` directory is the RTIQA engineering system foundation. It organizes the project’s long-term standards, architecture, AI tooling, and engineering knowledge.

This system is intended to support human contributors and future AI-assisted development by capturing RTIQA-specific engineering practices, design patterns, and generation tools.

## Directory overview

- `standards/` — engineering standards, coding conventions, and quality criteria.
- `blueprints/` — system blueprints and high-level design templates for RTIQA modules.
- `generators/` — generation recipes and automation scaffolds for common engineering assets.
- `prompts/` — reusable AI prompts for code generation, review, and design guidance.
- `templates/` — document, issue, and architecture templates that enforce RTIQA consistency.
- `rules/` — project rules, enforcement policies, and guardrails for engineering decisions.
- `architecture/` — core architecture models, diagrams, and design patterns.
- `decisions/` — architecture decision records and rationale tracking.
- `ai/` — AI-assisted engineering workflows, evaluation guidelines, and agent interaction models.

## Purpose

The `.rtiqa` system is the single source of engineering truth for RTIQA. It is designed to grow over time, enabling:

- consistent engineering standards
- structured decision-making
- scalable architecture planning
- AI-assisted development workflows
- repeatable project generation and governance

### Usage

- Contributors should consult `.rtiqa/README.md` first when making engineering decisions.
- AI agents should use `.rtiqa/prompts/` and `.rtiqa/generators/` as the structured engineering brain.
- Maintainers should update `.rtiqa/decisions/` with every major architectural or process decision.
