from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    PluginDefinition,
    ProjectDefinition,
    PROJECT_LIFECYCLE_STAGES,
    PROJECT_TYPES,
)


class ProjectLoader:
    """Load RTIQA project definition documents from disk."""

    def __init__(self, project_definition_path: Path) -> None:
        self.project_definition_path = project_definition_path

    def load_project_definition(self) -> ProjectDefinition:
        try:
            with self.project_definition_path.open("r", encoding="utf-8") as reader:
                payload = json.load(reader)
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Project definition not found: {self.project_definition_path}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in project definition {self.project_definition_path}: {exc}") from exc

        if not isinstance(payload, dict):
            raise ValueError("Project definition must be a JSON object.")

        project_id = self._require_string(payload, "id", self.project_definition_path)
        name = self._require_string(payload, "name", self.project_definition_path)
        version = self._validate_version(self._require_string(payload, "version", self.project_definition_path), self.project_definition_path, "version")
        schema_version = self._validate_version(self._require_string(payload, "schema_version", self.project_definition_path), self.project_definition_path, "schema_version")
        project_type = self._validate_project_type(self._require_string(payload, "project_type", self.project_definition_path))
        description = self._optional_string(payload, "description", default="")

        application_boundary = self._optional_mapping(payload, "application_boundary", self.project_definition_path)
        module_categories = self._optional_string_list(payload, "module_categories", self.project_definition_path)
        service_categories = self._optional_string_list(payload, "service_categories", self.project_definition_path)
        infrastructure_categories = self._optional_string_list(payload, "infrastructure_categories", self.project_definition_path)
        metadata = self._optional_mapping(payload, "metadata", self.project_definition_path)
        lifecycle = self._optional_mapping(payload, "lifecycle", self.project_definition_path)
        extensions = self._optional_mapping(payload, "extensions", self.project_definition_path)
        project_root = self._determine_project_root(self.project_definition_path)
        blueprint_root = self._resolve_resource_path(
            self._optional_nonempty_string(payload, "blueprint_root", default=".rtiqa/blueprints"),
            project_root,
        )
        template_root = self._resolve_resource_path(
            self._optional_nonempty_string(payload, "template_root", default=".rtiqa/templates"),
            project_root,
        )
        module_root = self._resolve_resource_path(
            self._optional_nonempty_string(payload, "module_root", default=".rtiqa/modules"),
            project_root,
        )
        output_root = self._resolve_resource_path(
            self._optional_nonempty_string(payload, "output_root", default="."),
            project_root,
        )

        plugins_payload = payload.get("plugins", [])
        if not isinstance(plugins_payload, list):
            raise ValueError(f"Project definition {self.project_definition_path} field plugins must be a list.")

        plugins = [self._parse_plugin(item, self.project_definition_path) for item in plugins_payload]
        self._validate_plugins(plugins, self.project_definition_path)
        self._validate_lifecycle(lifecycle, self.project_definition_path)

        return ProjectDefinition(
            id=project_id,
            name=name,
            description=description,
            version=version,
            schema_version=schema_version,
            project_type=project_type,
            application_boundary=application_boundary,
            module_categories=module_categories,
            service_categories=service_categories,
            infrastructure_categories=infrastructure_categories,
            metadata=metadata,
            lifecycle=lifecycle,
            extensions=extensions,
            blueprint_root=blueprint_root,
            template_root=template_root,
            module_root=module_root,
            output_root=output_root,
            plugins=plugins,
        )

    def _require_string(self, payload: Dict[str, Any], key: str, path: Path, default: Optional[Any] = None) -> str:
        value = payload.get(key, default)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Project definition {path} must include a non-empty string {key}.")
        return value

    def _optional_string(self, payload: Dict[str, Any], key: str, default: str = "") -> str:
        value = payload.get(key, default)
        if value is None:
            return default
        if not isinstance(value, str):
            raise ValueError(f"Project definition field {key} must be a string.")
        return value

    def _optional_nonempty_string(self, payload: Dict[str, Any], key: str, default: str = "") -> str:
        value = payload.get(key, default)
        if value is None:
            return default
        if not isinstance(value, str):
            raise ValueError(f"Project definition field {key} must be a string.")
        if value.strip() == "":
            raise ValueError(f"Project definition field {key} must not be empty.")
        return value

    def _optional_mapping(self, payload: Dict[str, Any], key: str, path: Path) -> Dict[str, Any]:
        value = payload.get(key, {})
        if not isinstance(value, dict):
            raise ValueError(f"Project definition {path} field {key} must be an object.")
        return value

    def _optional_string_list(self, payload: Dict[str, Any], key: str, path: Path) -> List[str]:
        value = payload.get(key, [])
        if not isinstance(value, list):
            raise ValueError(f"Project definition {path} field {key} must be a list.")
        if not all(isinstance(item, str) for item in value):
            raise ValueError(f"Project definition {path} field {key} must be a list of strings.")
        return value

    def _optional_bool(self, payload: Dict[str, Any], key: str, default: bool = False) -> bool:
        value = payload.get(key, default)
        if not isinstance(value, bool):
            raise ValueError(f"Project definition field {key} must be a boolean.")
        return value

    def _resolve_resource_path(self, value: str, parent: Path) -> Path:
        candidate = Path(value)
        if candidate.is_absolute():
            return candidate.resolve(strict=False)

        resolved = (parent / candidate).resolve(strict=False)
        if parent.resolve() not in resolved.parents and parent.resolve() != resolved:
            raise ValueError(f"Project definition {self.project_definition_path} path {value} escapes project root.")
        return resolved

    def _determine_project_root(self, project_definition_path: Path) -> Path:
        if project_definition_path.name == "project.json" and project_definition_path.parent.name == ".rtiqa":
            return project_definition_path.parent.parent.resolve()
        return project_definition_path.parent.resolve()

    def _validate_version(self, value: str, path: Path, key: str) -> str:
        pattern = r"^\d+\.\d+(?:\.\d+)?(?:[-+][0-9A-Za-z.-]+)?$"
        if not re.match(pattern, value):
            raise ValueError(f"Project definition {path} field {key} must follow semantic version format.")
        return value

    def _validate_project_type(self, project_type: str) -> str:
        if project_type not in PROJECT_TYPES:
            raise ValueError(f"Project type must be one of: {', '.join(sorted(PROJECT_TYPES))}.")
        return project_type

    def _validate_lifecycle(self, lifecycle: Dict[str, Any], path: Path) -> None:
        if not lifecycle:
            return
        stage = lifecycle.get("stage")
        if stage is not None:
            if not isinstance(stage, str):
                raise ValueError(f"Project definition {path} lifecycle.stage must be a string.")
            if stage not in PROJECT_LIFECYCLE_STAGES:
                raise ValueError(
                    f"Project definition {path} lifecycle.stage must be one of: {', '.join(sorted(PROJECT_LIFECYCLE_STAGES))}."
                )

    def _parse_plugin(self, item: Any, path: Path) -> PluginDefinition:
        if not isinstance(item, dict):
            raise ValueError(f"Project definition {path} plugins items must be objects.")

        plugin_id = self._require_string(item, "id", path)
        name = self._require_string(item, "name", path)
        version = self._validate_version(self._require_string(item, "version", path), path, "version")
        entrypoint = self._require_string(item, "entrypoint", path)
        description = self._optional_string(item, "description", default="")
        enabled = self._optional_bool(item, "enabled", default=True)
        configuration_schema = self._optional_mapping(item, "configuration_schema", path)
        metadata = self._optional_mapping(item, "metadata", path)

        return PluginDefinition(
            id=plugin_id,
            name=name,
            version=version,
            entrypoint=entrypoint,
            enabled=enabled,
            description=description,
            configuration_schema=configuration_schema,
            metadata=metadata,
        )

    def _validate_plugins(self, plugins: List[PluginDefinition], path: Path) -> None:
        from collections import Counter

        duplicates = [plugin_id for plugin_id, count in Counter(plugin.id for plugin in plugins).items() if count > 1]
        if duplicates:
            raise ValueError(
                f"Project definition {path} contains duplicate plugin ids: {', '.join(sorted(duplicates))}."
            )
