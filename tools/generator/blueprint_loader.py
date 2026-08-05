from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .models import Blueprint, FileArtifact
from .validator import validate_semantic_version


class BlueprintLoader:
    """Load generator blueprint definitions from disk."""

    def __init__(self, blueprint_root: Path) -> None:
        self.blueprint_root = blueprint_root

    def discover_blueprints(self) -> List[Blueprint]:
        blueprints: List[tuple[Blueprint, Path]] = []
        if not self.blueprint_root.exists():
            return []

        for path in sorted(self.blueprint_root.rglob("*.json")):
            blueprints.append((self.load_blueprint(path), path))

        self._check_duplicate_ids(blueprints)
        return [blueprint for blueprint, _ in blueprints]

    def load_blueprint(self, path: Path) -> Blueprint:
        try:
            with path.open("r", encoding="utf-8") as reader:
                payload = json.load(reader)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in blueprint {path}: {exc}") from exc

        if not isinstance(payload, dict):
            raise ValueError(f"Blueprint {path} must be a JSON object.")

        blueprint_id = self._require_string(payload, "id", path)
        name = self._require_string(payload, "name", path)
        version = validate_semantic_version(self._require_string(payload, "version", path), "version", path)
        schema_version = validate_semantic_version(self._require_string(payload, "schema_version", path), "schema_version", path)
        description = self._optional_string(payload, "description", default="")
        category = self._optional_string(payload, "category", default="")

        metadata = self._optional_mapping(payload, "metadata", path)
        metadata_schema = self._optional_mapping(payload, "metadata_schema", path)
        compatibility = self._optional_mapping(payload, "compatibility", path)
        outputs = self._optional_mapping(payload, "outputs", path)
        schema = self._optional_mapping(payload, "schema", path)
        variables = self._optional_mapping(payload, "variables", path)
        conditions = self._optional_list(payload, "conditions", path)
        dependencies = self._optional_string_list(payload, "dependencies", path)
        extends = self._optional_string_list(payload, "extends", path)
        compose = self._optional_string_list(payload, "compose", path)
        template_map = self._optional_mapping(payload, "template_map", path)
        directories = self._optional_string_list(payload, "directories", path)

        files_payload = payload.get("files", [])
        if not isinstance(files_payload, list):
            raise ValueError(f"Blueprint {path} files must be a list.")

        files = [self._parse_file_artifact(item, path) for item in files_payload]

        return Blueprint(
            id=blueprint_id,
            name=name,
            description=description,
            version=version,
            schema_version=schema_version,
            category=category,
            metadata=metadata,
            metadata_schema=metadata_schema,
            compatibility=compatibility,
            outputs=outputs,
            schema=schema,
            variables=variables,
            conditions=conditions,
            dependencies=dependencies,
            extends=extends,
            compose=compose,
            template_map=template_map,
            directories=directories,
            files=files,
        )

    def _require_string(self, payload: Dict[str, Any], key: str, path: Path, default: Any = None) -> str:
        value = payload.get(key, default)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Blueprint {path} must include a non-empty string {key}.")
        return value

    def _optional_string(self, payload: Dict[str, Any], key: str, default: str = "") -> str:
        value = payload.get(key, default)
        if value is None:
            return default
        if not isinstance(value, str):
            raise ValueError(f"Blueprint field {key} must be a string.")
        return value

    def _optional_mapping(self, payload: Dict[str, Any], key: str, path: Path) -> Dict[str, Any]:
        value = payload.get(key, {})
        if not isinstance(value, dict):
            raise ValueError(f"Blueprint {path} field {key} must be an object.")
        return value


    def _optional_list(self, payload: Dict[str, Any], key: str, path: Path) -> List[Dict[str, Any]]:
        value = payload.get(key, [])
        if not isinstance(value, list):
            raise ValueError(f"Blueprint {path} field {key} must be a list.")
        return value

    def _check_duplicate_ids(self, blueprint_entries: List[tuple[Blueprint, Path]]) -> None:
        duplicates: Dict[str, List[Path]] = {}
        for blueprint, path in blueprint_entries:
            duplicates.setdefault(blueprint.id, []).append(path)

        conflict_messages: List[str] = []
        for blueprint_id, paths in duplicates.items():
            if len(paths) > 1:
                conflict_messages.append(
                    f"{blueprint_id}: {', '.join(str(path) for path in paths)}"
                )

        if conflict_messages:
            raise ValueError(
                f"Duplicate blueprint ids discovered: {'; '.join(conflict_messages)}"
            )

    def _optional_string_list(self, payload: Dict[str, Any], key: str, path: Path) -> List[str]:
        value = payload.get(key, [])
        if not isinstance(value, list):
            raise ValueError(f"Blueprint {path} field {key} must be a list.")
        if not all(isinstance(item, str) for item in value):
            raise ValueError(f"Blueprint {path} field {key} must be a list of strings.")
        return value

    def _parse_file_artifact(self, item: Any, path: Path) -> FileArtifact:
        if not isinstance(item, dict):
            raise ValueError(f"Blueprint {path} file items must be objects.")

        path_value = item.get("path")
        template_name = item.get("template")
        condition = item.get("condition")

        if not isinstance(path_value, str) or not path_value.strip():
            raise ValueError(f"Blueprint {path} file item must include a non-empty string path.")
        if not isinstance(template_name, str) or not template_name.strip():
            raise ValueError(f"Blueprint {path} file item must include a non-empty string template.")

        variables = item.get("variables", {})
        if not isinstance(variables, dict):
            raise ValueError(f"Blueprint {path} file item variables must be an object.")

        if condition is not None and not isinstance(condition, str):
            raise ValueError(f"Blueprint {path} file item condition must be a string when provided.")

        return FileArtifact(
            path=path_value,
            template_name=template_name,
            variables=variables,
            condition=condition,
        )
