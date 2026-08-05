# Contributing to RTIQA

Welcome to RTIQA. This document describes how to contribute in a way that supports project stability, collaboration, and long-term maintainability.

## Table of Contents

- [Our values](#our-values)
- [How to contribute](#how-to-contribute)
- [Project roles](#project-roles)
- [Branch strategy](#branch-strategy)
- [Commit message guidelines](#commit-message-guidelines)
- [Pull request process](#pull-request-process)
- [Code standards](#code-standards)
- [Review process](#review-process)
- [Reporting issues](#reporting-issues)
- [Security reporting](#security-reporting)
- [Documentation expectations](#documentation-expectations)

## Our values

RTIQA is guided by these values:

- quality first
- inclusive collaboration
- open governance
- security by design
- transparency
- respect for contributors

## How to contribute

1. Review the project foundation material:
   - `README.md`
   - `docs/01_VISION.md`
   - `docs/05_ARCHITECTURE.md`
   - `GOVERNANCE.md`
2. Check existing issues and discussions for overlap.
3. Open an issue to propose large or architectural changes.
4. Create a focused branch and submit a pull request.

> RTIQA is in its foundation stage, so improvements to documentation, governance, and developer experience are especially valuable.

> Note: If you are new to the Frappe ecosystem, review `docs/11_SETUP.md` before contributing.

## Project roles

- **Maintainers**: approve and merge contributions, manage releases, and enforce project standards.
- **Contributors**: propose issues, submit pull requests, and improve documentation.
- **Reviewers**: provide technical feedback and verify that contributions meet project expectations.

## Branch strategy

- `main`: stable branch for release-ready content.
- `develop`: active development and integration.
- `feature/<name>`: new features or enhancements.
- `hotfix/<name>`: urgent fixes for `main`.
- `docs/<name>`: documentation changes.

## Commit message guidelines

Use clear, concise commit messages.

Recommended format:

`<type>(<scope>): <short description>`

Common types:

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation only changes
- `style`: formatting or non-functional changes
- `refactor`: code changes without behavior changes
- `perf`: performance improvements
- `test`: test-related changes
- `chore`: maintenance or tooling changes

Example:

`feat(deps): add automated dependency update workflow`

## Pull request process

1. Open an issue for large or architectural work.
2. Branch from `develop`.
3. Keep PRs small and focused.
4. Use the pull request template.
5. Describe the change, testing, and any follow-up work.
6. Include documentation updates when relevant.
7. Avoid modifying `infra/frappe_docker/` or Frappe core framework files without prior maintainer approval.
8. Run formatting and lint checks before requesting review.

## Code standards

### Python

- Format code with `black`.
- Lint with `ruff`.

### JavaScript / TypeScript

- Use `eslint` and `prettier` when applicable.

### Documentation

- Use clear, professional English.
- Keep documentation aligned with the codebase.
- Reference related docs for architecture, setup, and deployment.
- Update `ROADMAP.md` or `CHANGELOG.md` when the change affects project direction.

## Review process

Pull requests are reviewed by at least one maintainer.
Reviewers evaluate:

- correctness and reliability
- code quality and style
- documentation coverage
- security implications
- alignment with project principles

## Reporting issues

Use the templates in `.github/ISSUE_TEMPLATE/` for bugs, enhancements, and documentation changes.

Provide:

- a clear problem statement
- steps to reproduce
- expected vs actual behavior
- relevant environment details

## Security reporting

Do not disclose security issues in public issue threads.
Report them privately using the process in `SECURITY.md`.

## Documentation expectations

Every meaningful change should include documentation updates for:

- architecture changes
- API updates
- user-facing behavior
- deployment and setup instructions
