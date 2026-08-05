# Module System Specification

Version: 1.0

Status: Draft

---

## Overview

The RTIQA Module System defines a JSON-based module descriptor format for describing reusable architecture modules in the Rtiqa generator ecosystem. A module definition is a declarative contract that describes:

- module identity and versioning
- functional category and lifecycle stage
- capabilities and integration points
- external dependencies and compatibility requirements
- permission and event contracts
- validation expectations

This document is intended to allow another engineer to implement compatible modules without reading the generator source.

## Goals

- Provide a stable, predictable module descriptor format.
- Ensure module definitions are validated early, with clear errors.
- Support scalable and extensible module discovery for large projects.
- Keep module metadata extensible while preserving compatibility.
- Enable engine-driven dependency, lifecycle, and capability validation.

## Module Definition Structure

A module definition is a JSON object. Every module descriptor must be valid JSON and must be stored under the configured module root directory.

### Top-level fields

Supported top-level fields in a module definition:

- `id` (string, required)
- `name` (string, required)
- `description` (string, optional)
- `version` (string, required)
- `schema_version` (string, required)
- `module_type` (string, required)
- `module_category` (string, required)
- `module_categories` (array of strings, optional)
- `module_tags` (array of strings, optional)
- `metadata` (object, optional)
- `lifecycle` (object, optional)
- `capabilities` (object, optional)
- `service_integration` (object, optional)
- `api_integration` (object, optional)
- `database_integration` (object, optional)
- `ui_integration` (object, optional)
- `ai_integration` (object, optional)
- `permissions` (object, optional)
- `events` (object, optional)
- `extensions` (object, optional)
- `compatibility` (object, optional)
- `dependencies` (array of strings, optional)

### Required fields

#### `id`
- Unique module identifier.
- Must be a non-empty string.
- Must be unique across all discovered module definitions.
- Used in module dependency references.

#### `name`
- Human-readable module name.
- Used in reports and listing outputs.

#### `version`
- Module version string.
- Must follow semantic version format: `MAJOR.MINOR[.PATCH]`, optionally with prerelease/build metadata.

#### `schema_version`
- Schema version string for the module descriptor.
- Must follow semantic version format.
- Used during compatibility validation.

#### `module_type`
- Describes the technical role of the module.
- Must be one of the supported module types.

#### `module_category`
- Describes the logical category for the module.
- Must be one of the supported module categories.

## Supported Module Types

Supported values for `module_type`:

- `domain`
- `service`
- `integration`
- `utility`
- `data`
- `ui`
- `ai`
- `security`
- `infrastructure`

These values are used to classify modules by their primary architectural role.

## Supported Module Categories

Supported values for `module_category`:

- `core`
- `shared`
- `feature`
- `integration`
- `platform`
- `extension`
- `experimental`

Categories are used for organizing module inventories and for tooling that filters or groups modules.

## Module Lifecycle

The `lifecycle` object describes the maturity stage of a module.

Supported lifecycle stages:

- `definition`
- `design`
- `development`
- `testing`
- `deployment`
- `maintenance`
- `deprecated`
- `retirement`

Example:

```json
"lifecycle": {
  "stage": "development"
}
```

### Lifecycle semantics

- `definition`: module is being conceptually defined.
- `design`: module architecture is being designed.
- `development`: module implementation is in progress.
- `testing`: module is undergoing validation.
- `deployment`: module is ready for deployment.
- `maintenance`: module is stable and maintained.
- `deprecated`: module is no longer recommended for new work.
- `retirement`: module is being removed.

## Capabilities

The `capabilities` object declares the runtime and integration capabilities of the module.

Supported capability keys:

- `api`
- `database`
- `ui`
- `ai`
- `service`
- `security`
- `data`
- `integration`

Capabilities may be declared as a boolean or as an object.

Example:

```json
"capabilities": {
  "api": true,
  "database": {
    "type": "postgres"
  },
  "ui": true
}
```

### Capability validation rules

- `capabilities` must be an object if present.
- Each capability key must be one of the supported values.
- Each capability value must be either a boolean or an object.
- If a capability is declared and not explicitly set to `false`, required integration details must also be present.

## Integrations

Modules declare integration details in dedicated sub-objects.

### `service_integration`

Used for modules that expose or depend on service-level integration.

Example:

```json
"service_integration": {
  "endpoints": ["/users", "/accounts"]
}
```

### `api_integration`

Used for modules with API capabilities.

Example:

```json
"api_integration": {
  "routes": ["/users", "/login"]
}
```

### `database_integration`

Used for modules with database capabilities.

Example:

```json
"database_integration": {
  "tables": ["users", "accounts"]
}
```

### `ui_integration`

Used for modules with user interface capabilities.

Example:

```json
"ui_integration": {
  "pages": ["dashboard", "settings"]
}
```

### `ai_integration`

Used for modules that declare AI capabilities.

Example:

```json
"ai_integration": {
  "models": ["semantic-search"]
}
```

### Integration validation rules

- If `api_integration` is present, `capabilities.api` must not be explicitly `false`.
- If `database_integration` is present, `capabilities.database` must not be explicitly `false`.
- If `ui_integration` is present, `capabilities.ui` must not be explicitly `false`.
- If `ai_integration` is present, `capabilities.ai` must not be explicitly `false`.
- If `service_integration` is present, `capabilities.service` must not be explicitly `false`.

## Dependency Rules

The `dependencies` array lists other module `id`s that this module depends on.

Example:

```json
"dependencies": ["authentication", "data-access"]
```

### Dependency validation rules

- `dependencies` must be an array of strings.
- A module may not declare the same dependency more than once.
- A module may not depend on itself.
- All referenced dependency IDs must exist among discovered modules.
- Cyclic dependencies are invalid and cause module loading failure.

## Compatibility Rules

The `compatibility` object controls runtime validation for module compatibility.

Supported keys:

- `engine` (string)
- `schema_version` (string)

Example:

```json
"compatibility": {
  "engine": "^1.0.0",
  "schema_version": "~1.0"
}
```

### Compatibility semantics

- `engine` is matched against the generator engine version.
- `schema_version` is matched against the module's own `schema_version`.
- Supported version expressions:
  - exact: `1.0.0`
  - caret: `^1.0.0`
  - tilde: `~1.0`

Validation fails when the current runtime does not satisfy the declared compatibility expression.

## Permissions Model

The `permissions` object declares the permission contract for a module.

Example:

```json
"permissions": {
  "read": true,
  "write": {
    "scope": "admin"
  }
}
```

### Permissions validation rules

- `permissions` must be an object if present.
- Each key must be a string.
- Each value must be a boolean, object, or array.
- The module system does not enforce a specific schema inside `permissions`; it is preserved for tooling and later extension.

## Event Model

The `events` object declares event contracts emitted or consumed by the module.

Example:

```json
"events": {
  "user.created": {
    "schema": {
      "userId": "string"
    }
  }
}
```

### Events validation rules

- `events` must be an object if present.
- Each key must be a string.
- Each value must be an object.
- The engine preserves event definitions for tooling and does not impose a specific internal structure.

## Validation Rules

### Loader-level validation

The module loader enforces the following rules during file parsing:

- The module file must parse as valid JSON.
- The top-level payload must be an object.
- Required string fields must be present and non-empty: `id`, `name`, `version`, `schema_version`, `module_type`, `module_category`.
- `module_categories` and `module_tags` must be arrays of strings.
- `metadata`, `lifecycle`, `capabilities`, `service_integration`, `api_integration`, `database_integration`, `ui_integration`, `ai_integration`, `permissions`, `events`, `extensions`, `compatibility` must be objects when present.
- `dependencies` must be an array of strings.

### Module validator rules

The module validator applies additional production rules:

- `module_type` must be one of the supported module types.
- `module_category` must be one of the supported module categories.
- `lifecycle.stage` must be one of the supported lifecycle stages.
- `capabilities` must be an object with supported keys.
- If capability keys are present, values must be boolean or object.
- Capability/integration relationships must be consistent:
  - API integration requires `api` capability.
  - Database integration requires `database` capability.
  - UI integration requires `ui` capability.
  - AI integration requires `ai` capability.
  - Service integration requires `service` capability.
- `permissions` values must be boolean, object, or list.
- `events` values must be objects.
- Modules cannot depend on themselves.
- Duplicate dependency entries are invalid.

### Engine-level validation

The generator engine validates entire module graphs during discovery and reload:

- Each discovered module must be valid on its own.
- All declared module dependencies must exist.
- Module dependency cycles are detected and rejected.
- Module compatibility expressions are evaluated against engine and schema versions.
- Duplicate module IDs across files are rejected.

## Module Discovery

### Module root

Module definitions are discovered under the configured module root directory.

- Default root: `.rtiqa/modules`
- Configured in project definition via `module_root`.
- If the root is not present, discovery returns an empty module set.

### File discovery

- The module loader discovers module files recursively using a depth-first search.
- Only files with a `.json` extension are considered.
- Every discovered file is loaded, parsed, and validated.
- Duplicate module IDs discovered across any module file are rejected.

## Module Loading

### Load process

1. Discover JSON files under module root.
2. Parse each file into a JSON object.
3. Validate top-level types and required fields.
4. Construct a `ModuleDefinition` object.
5. Validate lifecycle, capabilities, integrations, permissions, events, and dependencies.
6. Validate compatibility expressions.
7. Validate dependency graph for missing references and cycles.

### Error reporting

Validation errors include:

- file path location
- field-level failure reason
- module ID context where available
- duplicate module ID or duplicate dependency details
- cycle detection paths for module dependencies

Example error forms:

- `Invalid JSON in module definition /path/to/module.json: ...`
- `Module definition /path/to/module.json must include a non-empty string id.`
- `Unsupported capability: badcapability`
- `api_integration defined without api capability.`
- `Module dependencies not found: authentication`
- `Module dependency cycle detected: a -> b -> a`
- `Module validation failed: user-service: ...`

## Best Practices

- Choose globally unique `id` values.
- Keep module IDs short, stable, and descriptive.
- Prefer explicit `capabilities` declarations rather than relying on undocumented behavior.
- Always include integration details when declaring capabilities.
- Use `dependencies` to model explicit module relationships.
- Keep dependency graphs acyclic and shallow when possible.
- Use `lifecycle.stage` to communicate maturity and release readiness.
- Store non-execution metadata in `metadata` and leave behavior to tooling.
- Use `permissions` and `events` as declarative contracts, not executable logic.
- Document custom fields inside `extensions` instead of polluting core fields.
- Avoid using `experimental` category for production-critical modules.

## Future Extension Points

The module system is intentionally designed to be extensible.

Possible future extensions:

- `module_schema`: add per-module input validation schema.
- `metadata_schema`: add schema validation for module metadata.
- `configuration_schema`: support module-specific configuration payloads.
- `implementation` or `source` fields for module artifact generation hooks.
- `module_exports`: declare outputs provided by the module.
- richer event contract validation and event payload typing.
- dependency versioning or compatibility ranges.
- module capability profiling and runtime enforcement.
- `environment` sections for deployment-specific metadata.
- `conditions` and `policies` for conditional module activation.

## Example Module Definition

```json
{
  "id": "user-service",
  "name": "User Service",
  "description": "Provides user management APIs and data access.",
  "version": "1.0.0",
  "schema_version": "1.0",
  "module_type": "service",
  "module_category": "feature",
  "module_categories": ["feature", "shared"],
  "module_tags": ["users", "auth"],
  "metadata": {
    "owner": "platform-team"
  },
  "lifecycle": {
    "stage": "development"
  },
  "capabilities": {
    "api": true,
    "database": true,
    "service": true
  },
  "service_integration": {
    "endpoints": ["/users"]
  },
  "api_integration": {
    "routes": ["/users", "/users/{id}"]
  },
  "database_integration": {
    "tables": ["users"]
  },
  "permissions": {
    "read": true,
    "write": {
      "scope": "admin"
    }
  },
  "events": {
    "user.created": {
      "description": "Emitted when a new user is created."
    }
  },
  "compatibility": {
    "engine": "^1.0.0",
    "schema_version": "~1.0"
  },
  "dependencies": ["auth-service", "data-store"]
}
```

## Summary

The RTIQA Module System is a validated, JSON-driven descriptor format designed for architectural module interoperability. It supports explicit type, capability, integration, lifecycle, permission, and event metadata, while also enforcing dependency and compatibility rules. This specification should allow engineers to author compatible modules without inspecting the generator implementation.
