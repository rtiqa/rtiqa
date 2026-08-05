# RTIQA Database Generator

This document defines the RTIQA database generator. It generates database schemas, migration artifacts, and storage integration for new modules.

## Purpose

The database generator creates data persistence definitions and ensures schema design aligns with RTIQA architecture and Frappe conventions.

## Inputs

- `database_name`: Optional database schema name or namespace.
- `module_context`: Owning module or app.
- `entities`: Entity definitions, fields, relationships, and constraints.
- `indexes`: Index and performance guidance.
- `storage_policy`: Data retention, partitioning, and security classification.
- `integration_requirements`: External data sources or replication needs.

## Outputs

- data model definitions (Frappe DocTypes, schema migration files, SQL DDL templates)
- migration and seed scripts
- metadata for data lineage and ownership
- storage and access policy documentation

## Dependencies

- `generator-registry` for discovery
- `module-generator` or `api-generator` for owning context
- `documentation-generator` for schema docs
- `test-generator` for data validation tests

## Validation

- Verify entity names and field definitions follow naming conventions.
- Validate relational integrity and required constraints.
- Ensure storage and security policies are declared.
- Confirm generated schema is compatible with Frappe data model rules.

## Execution flow

1. Validate entity model inputs.
2. Generate schema definitions and migration artifacts.
3. Create seed or example data if needed.
4. Wire persistence metadata into module definitions.
5. Generate schema documentation and tests.
6. Run validation checks.

## Extension mechanism

- Support multiple persistence backends (MariaDB, PostgreSQL, NoSQL).
- Allow custom migration template injection.
- Enable domain-specific schema review hooks.

## Why this generator exists

The database generator ensures data models are generated consistently and safely, reducing the risk of ungoverned schema drift in RTIQA projects.
