# RTIQA Generator Workflow

This document defines the workflow for running RTIQA generators. It is the operational playbook for generating engineering artifacts.

## Purpose

The generator workflow describes the end-to-end process from generator discovery to artifact validation. It ensures consistent execution across RTIQA generator runs.

## Workflow steps

### 1. Registry discovery

- The framework discovers available generators by reading registry metadata.
- It validates generator metadata against `generator-spec.md`.
- Discovered generators are categorized and made available for execution.

### 2. Input collection

- The workflow collects input data from user prompts, project metadata, and existing repository state.
- Inputs are normalized against each generator’s declared input schema.
- Incomplete or invalid input data is rejected before execution.

### 3. Dependency resolution

- The resolver reads generator dependencies and constructs an execution graph.
- Generators are scheduled in dependency order.
- Cyclic dependencies are flagged as errors and must be resolved.

### 4. Pre-run validation

- Each generator validates its inputs.
- The workflow checks dependency readiness.
- If a generator fails validation, the workflow halts with a clear error.

### 5. Generator execution

- The execution engine runs each generator in order.
- Generators follow their defined execution flow.
- Extension hooks may run before or after generator execution.

### 6. Output registration

- Generators register produced artifacts in the shared artifact store.
- Outputs are recorded with metadata, including source generator, timestamp, and validation status.

### 7. Post-run validation

- Generators run validation checks against generated outputs.
- The workflow ensures outputs conform to naming, formatting, and architecture rules.
- Validation failures produce actionable diagnostics.

### 8. Reporting

- The workflow summarizes generated artifacts, validation results, and any unmet dependencies.
- Reports are suitable for review by maintainers, contributors, and AI agents.

## Extension points

The workflow includes hook points for:

- pre-discovery
- pre-validation
- pre-execution
- post-execution
- post-validation

Extensions can add custom logging, policy enforcement, or alternate validation rules.

## Why this workflow exists

A repeatable, deterministic workflow reduces the risk of inconsistent generator behavior. It also makes the generator framework suitable for both human-driven and AI-assisted engineering operations.
