# RTIQA Generator Architecture

This document defines the architecture of the RTIQA generator framework. It describes how individual generators are organized, discovered, and composed to produce engineering artifacts.

## Purpose

The generator architecture provides a language-agnostic blueprint for how RTIQA generators interact. It ensures the framework is modular, extensible, and usable by both AI agents and human developers.

## Architectural components

### Generator definition

Each generator is defined by metadata that conforms to the RTIQA generator specification. This metadata is discoverable by the generator registry.

### Generator registry

The registry is the central catalog that discovers available generators, their categories, dependencies, and execution contracts.

### Dependency resolver

The resolver computes the execution order of generators based on declared dependencies. It ensures required generators are executed before dependent generators.

### Execution engine

The execution engine runs generators by following their declared execution flow. It handles input validation, extension hooks, artifact creation, and post-generation validation.

### Extension layer

The extension layer provides hook points and adapters that allow new behaviors to be added without modifying existing generators.

## Communication model

Generators communicate through structured artifacts and registry metadata rather than direct function calls.

### Input/output contracts

- A generator consumes inputs and produces outputs described in its metadata.
- Outputs from one generator become input sources for dependent generators.
- The framework uses an artifact graph to track produced resources.

### Event-driven coordination

- The execution engine emits events at key stages: pre-run, post-run, validation start, and validation complete.
- Extensions can subscribe to events without changing generator internals.

### Shared artifact store

The framework maintains a shared artifact store where generated artifacts are tracked.
- Generators register outputs in the artifact store after successful generation.
- Dependent generators query the artifact store for required inputs.

## Modular design

The architecture is intentionally modular:

- Each generator is independent and self-describing.
- New generators are added through the registry without modifications to existing generators.
- Extensions plug into the execution engine and generator lifecycle.

## RTIQA-specific constraints

- Generators must respect `.rtiqa/rules/architecture-rules.md` and `.rtiqa/rules/ai-development-rules.md`.
- Generated artifacts should adhere to RTIQA naming and repository structure standards.
- The framework must support RTIQA engineering artifacts in addition to code generation.

## Why this architecture exists

RTIQA needs a generator framework that can evolve without requiring a full rewrite. This architecture supports incremental growth and enables AI-assisted workflows to be introduced in a controlled, auditable way.
