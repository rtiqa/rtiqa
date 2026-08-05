from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .models import (
    ModuleDefinition,
    MODULE_CATEGORIES,
    MODULE_LIFECYCLE_STAGES,
    MODULE_TYPES,
)
from .validator import validate_semantic_version


class ModuleLoader:
    """Load RTIQA module definitions from disk."""

    def __init__(self, module_root: Path) -> None:
        self.module_root = module_root

    def discover_modules(self) -> List[ModuleDefinition]:
        modules: List[ModuleDefinition] = []
        if not self.module_root.exists():
            return modules

        module_entries: List[tuple[ModuleDefinition, Path]] = []
        for path in sorted(self.module_root.rglob("*.json")):
            module_entries.append((self.load_module(path), path))

        self._check_duplicate_ids(module_entries)
        return [module for module, _ in module_entries]

    def load_module(self, path: Path) -> ModuleDefinition:
        try:
            with path.open("r", encoding="utf-8") as reader:
                payload = json.load(reader)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in module definition {path}: {exc}") from exc

        if not isinstance(payload, dict):
            raise ValueError(f"Module definition {path} must be a JSON object.")

        module_id = self._require_string(payload, "id", path)
        name = self._require_string(payload, "name", path)
        version = validate_semantic_version(self._require_string(payload, "version", path), "version", path)
        schema_version = validate_semantic_version(self._require_string(payload, "schema_version", path), "schema_version", path)
        module_type = self._validate_module_type(self._require_string(payload, "module_type", path), path)
        module_category = self._validate_module_category(self._require_string(payload, "module_category", path), path)
        description = self._optional_string(payload, "description", default="")

        module_categories = self._optional_string_list(payload, "module_categories", path)
        module_tags = self._optional_string_list(payload, "module_tags", path)
        metadata = self._optional_mapping(payload, "metadata", path)
        lifecycle = self._optional_mapping(payload, "lifecycle", path)
        capabilities = self._optional_mapping(payload, "capabilities", path)
        service_integration = self._optional_mapping(payload, "service_integration", path)
        api_integration = self._optional_mapping(payload, "api_integration", path)
        database_integration = self._optional_mapping(payload, "database_integration", path)
        ui_integration = self._optional_mapping(payload, "ui_integration", path)
        ai_integration = self._optional_mapping(payload, "ai_integration", path)
        permissions = self._optional_mapping(payload, "permissions", path)
        events = self._optional_mapping(payload, "events", path)
        extensions = self._optional_mapping(payload, "extensions", path)
        compatibility = self._optional_mapping(payload, "compatibility", path)
        dependencies = self._optional_string_list(payload, "dependencies", path)

        self._validate_lifecycle(lifecycle, path)

        return ModuleDefinition(
            id=module_id,
            name=name,
            description=description,
            version=version,
            schema_version=schema_version,
            module_type=module_type,
            module_category=module_category,
            module_categories=module_categories,
            module_tags=module_tags,
            metadata=metadata,
            lifecycle=lifecycle,
            capabilities=capabilities,
            service_integration=service_integration,
            api_integration=api_integration,
            database_integration=database_integration,
            ui_integration=ui_integration,
            ai_integration=ai_integration,
            permissions=permissions,
            events=events,
            extensions=extensions,
            compatibility=compatibility,
            dependencies=dependencies,
        )

    def _require_string(self, payload: Dict[str, Any], key: str, path: Path, default: Any = None) -> str:
        value = payload.get(key, default)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Module definition {path} must include a non-empty string {key}.")
        return value

    def _optional_string(self, payload: Dict[str, Any], key: str, default: str = "") -> str:
        value = payload.get(key, default)
        if value is None:
            return default
        if not isinstance(value, str):
            raise ValueError(f"Module definition {path} field {key} must be a string.")
        return value

    def _optional_mapping(self, payload: Dict[str, Any], key: str, path: Path) -> Dict[str, Any]:
        value = payload.get(key, {})
        if not isinstance(value, dict):
            raise ValueError(f"Module definition {path} field {key} must be an object.")
        return value

    def _optional_string_list(self, payload: Dict[str, Any], key: str, path: Path) -> List[str]:
        value = payload.get(key, [])
        if not isinstance(value, list):
            raise ValueError(f"Module definition {path} field {key} must be a list.")
        if not all(isinstance(item, str) for item in value):
            raise ValueError(f"Module definition {path} field {key} must be a list of strings.")
        return value


    def _validate_module_type(self, module_type: str, path: Path) -> str:
        if module_type not in MODULE_TYPES:
            raise ValueError(f"Module definition {path} module_type must be one of: {', '.join(sorted(MODULE_TYPES))}.")
        return module_type

    def _validate_module_category(self, module_category: str, path: Path) -> str:
        if module_category not in MODULE_CATEGORIES:
            raise ValueError(f"Module definition {path} module_category must be one of: {', '.join(sorted(MODULE_CATEGORIES))}.")
        return module_category

    def _validate_lifecycle(self, lifecycle: Dict[str, Any], path: Path) -> None:
        if not lifecycle:
            return
        stage = lifecycle.get("stage")
        if stage is not None:
            if not isinstance(stage, str):
                raise ValueError(f"Module definition {path} lifecycle.stage must be a string.")
            if stage not in MODULE_LIFECYCLE_STAGES:
                raise ValueError(
                    f"Module definition {path} lifecycle.stage must be one of: {', '.join(sorted(MODULE_LIFECYCLE_STAGES))}."
                )

    def _check_duplicate_ids(self, module_entries: List[tuple[ModuleDefinition, Path]]) -> None:
        duplicates: Dict[str, List[Path]] = {}
        for module, path in module_entries:
            duplicates.setdefault(module.id, []).append(path)

        conflict_messages: List[str] = []
        for module_id, paths in duplicates.items():
            if len(paths) > 1:
                conflict_messages.append(
                    f"{module_id}: {', '.join(str(path) for path in paths)}"
                )

        if conflict_messages:
            raise ValueError(
                f"Duplicate module ids discovered: {'; '.join(conflict_messages)}"
            )
