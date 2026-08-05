from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .models import Blueprint, FileArtifact


class BlueprintLoader:
    """Load generator blueprint definitions from disk."""

    def __init__(self, blueprint_root: Path) -> None:
        self.blueprint_root = blueprint_root

    def discover_blueprints(self) -> List[Blueprint]:
        blueprints: List[Blueprint] = []
        if not self.blueprint_root.exists():
            return blueprints

        for path in sorted(self.blueprint_root.glob("*.json")):
            blueprints.append(self.load_blueprint(path))

        return blueprints

    def load_blueprint(self, path: Path) -> Blueprint:
        try:
            with path.open("r", encoding="utf-8") as reader:
                payload = json.load(reader)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in blueprint {path}: {exc}") from exc

        if not isinstance(payload, dict):
            raise ValueError(f"Blueprint {path} must be a JSON object.")

        name = payload.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Blueprint {path} must include a non-empty string name.")

        schema = payload.get("schema", {})
        if not isinstance(schema, dict):
            raise ValueError(f"Blueprint {path} schema must be an object.")

        directories = payload.get("directories", [])
        if not isinstance(directories, list):
            raise ValueError(f"Blueprint {path} directories must be a list.")

        files_payload = payload.get("files", [])
        if not isinstance(files_payload, list):
            raise ValueError(f"Blueprint {path} files must be a list.")

        files = []
        for item in files_payload:
            if not isinstance(item, dict):
                raise ValueError(f"Blueprint {path} file items must be objects.")

            path_value = item.get("path")
            template_name = item.get("template")
            variables = item.get("variables", {})
            if not isinstance(path_value, str) or not isinstance(template_name, str):
                raise ValueError(f"Blueprint {path} file item must include string `path` and `template`.")

            if not isinstance(variables, dict):
                raise ValueError(f"Blueprint {path} file item `variables` must be an object.")

            files.append(
                FileArtifact(
                    path=path_value,
                    template_name=template_name,
                    variables=variables,
                )
            )

        return Blueprint(
            name=name,
            description=payload.get("description", ""),
            schema=schema,
            directories=directories,
            files=files,
        )
