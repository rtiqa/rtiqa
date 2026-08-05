from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from tools.generator.engine import GeneratorEngine
from tools.generator.models import ProjectDefinition
from tools.generator.project_loader import ProjectLoader


def test_project_loader_valid_definition(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    monkeypatch.chdir(project_root)

    project_definition = {
        "id": "rtiqa-sample",
        "name": "RTIQA Sample Project",
        "description": "A sample RTIQA project definition.",
        "version": "1.0.0",
        "schema_version": "1.0",
        "project_type": "application",
        "application_boundary": {
            "frontend": "web",
            "backend": "python",
        },
        "module_categories": ["domain", "infrastructure"],
        "service_categories": ["api", "batch"],
        "infrastructure_categories": ["database", "cache"],
        "metadata": {"owner": "platform-team", "tags": ["generator"]},
        "lifecycle": {"stage": "development"},
        "extensions": {"custom": True},
        "blueprint_root": "blueprints",
        "template_root": "templates",
        "output_root": "output",
        "plugins": [
            {
                "id": "project-reporter",
                "name": "Project Reporter",
                "version": "1.0.0",
                "entrypoint": "reporter:main",
                "enabled": True,
            }
        ],
    }

    path = project_root / ".rtiqa" / "project.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(project_definition, indent=2), encoding="utf-8")

    loaded = ProjectLoader(path).load_project_definition()

    assert isinstance(loaded, ProjectDefinition)
    assert loaded.id == "rtiqa-sample"
    assert loaded.project_type == "application"
    assert loaded.lifecycle["stage"] == "development"
    assert loaded.plugins[0].entrypoint == "reporter:main"


def test_engine_from_project_definition_loads_blueprints(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    monkeypatch.chdir(project_root)

    project_definition = {
        "id": "rtiqa-sample",
        "name": "RTIQA Sample Project",
        "version": "1.0.0",
        "schema_version": "1.0",
        "project_type": "application",
        "blueprint_root": "blueprints",
        "template_root": "templates",
        "output_root": "output",
        "plugins": [],
    }

    project_path = project_root / ".rtiqa" / "project.json"
    project_path.parent.mkdir(parents=True, exist_ok=True)
    project_path.write_text(json.dumps(project_definition, indent=2), encoding="utf-8")

    blueprint_root = project_root / "blueprints"
    template_root = project_root / "templates"
    output_root = project_root / "output"
    blueprint_root.mkdir()
    template_root.mkdir()
    output_root.mkdir()

    (blueprint_root / "dummy.json").write_text(
        json.dumps(
            {
                "id": "dummy",
                "name": "Dummy Blueprint",
                "version": "1.0.0",
                "schema_version": "1.0",
                "schema": {"required": {"project_name": "string"}},
                "files": [{"path": "dummy.txt", "template": "dummy.tpl"}],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    (template_root / "dummy.tpl").write_text("Dummy {project_name}\n", encoding="utf-8")

    engine = GeneratorEngine.from_project_definition(project_path)

    assert engine.project_definition is not None
    assert engine.project_definition.id == "rtiqa-sample"
    assert any(blueprint.id == "dummy" for blueprint in engine.list_blueprints())


def test_project_loader_resolves_relative_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    monkeypatch.chdir(project_root)

    project_definition = {
        "id": "relative-paths",
        "name": "Relative Paths Project",
        "version": "1.0.0",
        "schema_version": "1.0",
        "project_type": "application",
        "blueprint_root": "config/blueprints",
        "template_root": "config/templates",
        "output_root": "dist",
        "plugins": [],
    }

    project_path = project_root / ".rtiqa" / "project.json"
    project_path.parent.mkdir(parents=True, exist_ok=True)
    project_path.write_text(json.dumps(project_definition, indent=2), encoding="utf-8")

    loaded = ProjectLoader(project_path).load_project_definition()

    assert loaded.blueprint_root == (project_root / "config" / "blueprints").resolve()
    assert loaded.template_root == (project_root / "config" / "templates").resolve()
    assert loaded.output_root == (project_root / "dist").resolve()


def test_project_loader_detects_duplicate_plugins(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    monkeypatch.chdir(project_root)

    project_definition = {
        "id": "duplicate-plugins",
        "name": "Duplicate Plugins Project",
        "version": "1.0.0",
        "schema_version": "1.0",
        "project_type": "service",
        "blueprint_root": "blueprints",
        "template_root": "templates",
        "output_root": "output",
        "plugins": [
            {
                "id": "dup",
                "name": "Dup Plugin A",
                "version": "1.0.0",
                "entrypoint": "a:run",
                "enabled": True,
            },
            {
                "id": "dup",
                "name": "Dup Plugin B",
                "version": "1.0.0",
                "entrypoint": "b:run",
                "enabled": True,
            },
        ],
    }

    project_path = project_root / ".rtiqa" / "project.json"
    project_path.parent.mkdir(parents=True, exist_ok=True)
    project_path.write_text(json.dumps(project_definition, indent=2), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate plugin ids"):
        ProjectLoader(project_path).load_project_definition()
