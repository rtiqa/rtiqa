# RTIQA Generator Registry

This document defines the generator registry for RTIQA. The registry is the central catalog for discoverable generators.

## Purpose

The registry enables automatic discovery, dependency analysis, and execution orchestration for RTIQA generators.

## Registry responsibilities

- discover available generator definitions
- validate generator metadata against `generator-spec.md`
- track generator categories and versions
- resolve generator dependencies
- expose a query interface for execution orchestration

## Registry design

### Generator metadata

Each generator registers with the following metadata:

- `id`: unique generator identifier
- `name`: human-readable name
- `version`: semantic version or schema version
- `category`: generator category
- `description`: short summary
- `inputs`: required and optional inputs
- `outputs`: declared outputs
- `dependencies`: required generator or artifact dependencies
- `validation`: rules used for artifact verification
- `execution_flow`: steps the generator performs
- `extensions`: supported extension hooks

### Discovery mechanisms

The registry supports two discovery mechanisms:

1. file-based discovery
   - generator definitions are stored as metadata files in `.rtiqa/generators/`
   - the registry reads the metadata files and validates them

2. plugin-based discovery
   - new generators can register themselves with the registry through a plugin interface
   - the registry discovers plugins from a configured path or manifest

### Dependency resolution

- The registry builds a directed graph from generator dependencies.
- It detects cycles and missing dependencies.
- It exposes the execution order to the generator workflow.

### Versioning

- Generators may include a `version` field.
- The registry can support multiple versions of the same generator for compatibility and migration.

### Query interface

The registry should support queries such as:

- list all available generators
- find generators by category
- find generators that produce a given artifact
- get generator metadata by id

## Extensibility

- New generators can be added by introducing a metadata file under `.rtiqa/generators/`.
- Existing generators do not need to be modified when new generators are added.
- Extensions can add metadata enrichment without changing the registry core.

## Why this registry exists

The registry allows RTIQA to scale its generator system without hard-coded orchestration. It enables discovery and composition of independent generator artifacts in a robust, maintainable way.
