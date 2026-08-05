# RTIQA Generator Specification

This document defines the specification for RTIQA generators. It establishes the common contract that all RTIQA generator assets must follow.

## Purpose

The RTIQA generator specification defines how generators describe their capabilities, inputs, outputs, dependencies, validation requirements, execution flow, and extension points.

This enables a modular system architecture where generators are discoverable and interoperable, without requiring code-level coupling.

## Generator contract

Each generator must expose the following metadata:

- `name`: A unique generator identifier, such as `project-generator` or `api-generator`.
- `description`: A concise statement of the generator's responsibility.
- `version`: A semantic version string or schema version.
- `category`: Logical category, such as `project`, `module`, `api`, `database`, `documentation`, `ui`, `test`, or `deployment`.
- `inputs`: A formal definition of the data and configuration required to run the generator.
- `outputs`: A formal definition of the generated artifacts or artifacts to be updated.
- `dependencies`: A list of other generators or resources required prior to execution.
- `validation`: Rules or checks that must pass before the generator is considered successful.
- `execution_flow`: A step-by-step flow for running the generator.
- `extensions`: How additional behaviors or customizations can be attached.

## Inputs

Generator inputs are the source data the generator consumes. Inputs must be specific, structured, and documented.

Common input types for RTIQA generators include:

- project metadata: name, description, target architecture
- module definitions: business domain, scope, feature boundaries
- API contracts: endpoints, methods, request/response schema
- database schema: data models and relationships
- documentation requirements: audience, purpose, and format
- UI requirements: page types, user journeys, and component contracts
- deployment environment: container, service, or infrastructure profile

Generators should support input validation and reject incomplete or invalid input sets.

## Outputs

Generator outputs are the artifacts produced or updated by the generator.

Outputs may include:

- source file references
- documentation pages
- API specs
- database schema definitions
- module blueprints
- test plans
- deployment manifest fragments

Each generator must describe its expected outputs clearly.

## Dependencies

Generators declare dependencies on other generators or shared resources.

Dependencies allow the RTIQA generator framework to execute generators in the correct order and ensure required artifacts are available.

Example dependency relationships:

- `api-generator` depends on `module-generator`
- `database-generator` depends on `module-generator`
- `documentation-generator` depends on `project-generator` and `api-generator`

## Validation

Validation defines the conditions that must be met for the generator to succeed.

Validation may include:

- schema conformance checks
- naming convention validation
- architecture boundary checks
- dependency availability
- output completeness and artifact integrity

Validation must be explicit and reportable.

## Execution flow

Each generator must define an execution flow that includes:

1. input validation
2. dependency resolution
3. artifact generation planning
4. artifact creation or update
5. post-generation validation
6. reporting results

## Extension mechanism

The generator framework must support extensions without modifying existing generators.

Extension capabilities include:

- parameter injection: custom runtime options passed into generator execution
- hook points: pre-run and post-run extension hooks
- generator adapters: wrappers that transform input or output shapes
- plugin discovery: automatic discovery of new generator definitions

## RTIQA-specific guidelines

- Generators should behave as engineering assistants, producing design and governance artifacts in addition to source scaffolding.
- Generators must never bypass `.rtiqa/` engineering rules.
- Generators must respect RTIQA module boundaries and deployment patterns.

## Why this exists

A shared generator specification enables RTIQA to scale its engineering system consistently. It is the foundation for a future code generation layer that is safe, predictable, and aligned with RTIQA project engineering principles.
