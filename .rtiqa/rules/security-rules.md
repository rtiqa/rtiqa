# RTIQA Security Rules

This document defines the security rules for RTIQA engineering and development.

## Purpose

RTIQA handles sensitive educational and AI data. These rules ensure security is built into engineering workflows from the start.

## Rule set

### 1. Do not store secrets in source control

Never commit API keys, passwords, or credentials. Use environment variables and configuration management for sensitive values.

### 2. Validate external integrations

Document and validate any third-party integrations in `docs/09_AI_SYSTEM.md` or `docs/08_API.md`. Review the security impact of each external dependency.

### 3. Follow least privilege

Use the minimum required permissions for service accounts, API keys, and deployment credentials.

### 4. Secure data in transit and at rest

Ensure recommended encryption practices for all communication and storage. Document secure deployment recommendations in `docs/13_SECURITY.md`.

### 5. Review security for AI-generated outputs

AI-generated code and documentation must be reviewed for security implications before merging.

### 6. Report security issues privately

Use `SECURITY.md` for security reporting. Do not disclose vulnerabilities in public issues until coordinated disclosure is established.

## Why these rules exist

RTIQA’s value depends on trust. Strict security rules protect users, maintainers, and the project’s reputation.
