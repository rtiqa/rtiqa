from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from tools.generator.engine import GeneratorEngine
from tools.generator.module_loader import ModuleLoader
from tools.generator.models import ModuleDefinition
from tools.generator.project_loader import ProjectLoader


def test_module_loader_discovers_modules(tmp_path: Path) -> None:
    module_root = tmp_path / "modules"
    module_root.mkdir()

    module_definition = {
        "id": "user-service",
        "name": "User Service",
        "version": "1.0.0",
        "schema_version": "1.0",
        "module_type": "service",
        "module_category": "feature",
        "metadata": {"owner": "platform"},
        "capabilities": {"api": True},
        "api_integration": {"routes": ["/users"]},
    }

    path = module_root / "user-service.json"
    path.write_text(json.dumps(module_definition, indent=2), encoding="utf-8")

    loader = ModuleLoader(module_root)
    modules = loader.discover_modules()

    assert len(modules) == 1
    assert isinstance(modules[0], ModuleDefinition)
    assert modules[0].id == "user-service"
    assert modules[0].module_type == "service"
    assert modules[0].api_integration["routes"] == ["/users"]


def test_project_loader_resolves_module_root(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    project_definition = {
        "id": "module-paths",
        "name": "Module Paths Project",
        "version": "1.0.0",
        "schema_version": "1.0",
        "project_type": "application",
        "module_root": "config/modules",
        "blueprint_root": "blueprints",
        "template_root": "templates",
        "output_root": "dist",
        "plugins": [],
    }

    project_path = project_root / ".rtiqa" / "project.json"
    project_path.parent.mkdir(parents=True, exist_ok=True)
    project_path.write_text(json.dumps(project_definition, indent=2), encoding="utf-8")

    loaded = ProjectLoader(project_path).load_project_definition()
    assert loaded.module_root == (project_root / "config" / "modules").resolve()


def test_engine_from_project_definition_loads_modules(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    project_definition = {
        "id": "rtiqa-sample",
        "name": "RTIQA Sample Project",
        "version": "1.0.0",
        "schema_version": "1.0",
        "project_type": "application",
        "blueprint_root": "blueprints",
        "template_root": "templates",
        "module_root": "modules",
        "output_root": "output",
        "plugins": [],
    }

    project_path = project_root / ".rtiqa" / "project.json"
    project_path.parent.mkdir(parents=True, exist_ok=True)
    project_path.write_text(json.dumps(project_definition, indent=2), encoding="utf-8")

    blueprint_root = project_root / "blueprints"
    template_root = project_root / "templates"
    module_root = project_root / "modules"
    output_root = project_root / "output"
    blueprint_root.mkdir()
    template_root.mkdir()
    module_root.mkdir()
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

    module_definition = {
        "id": "user-service",
        "name": "User Service",
        "version": "1.0.0",
        "schema_version": "1.0",
        "module_type": "service",
        "module_category": "feature",
        "capabilities": {"api": True},
        "api_integration": {"routes": ["/users"]},
    }
    (module_root / "user-service.json").write_text(json.dumps(module_definition, indent=2), encoding="utf-8")

    engine = GeneratorEngine.from_project_definition(project_path)
    assert engine.project_definition is not None
    assert any(module.id == "user-service" for module in engine.list_modules())


def test_module_loader_discovers_nested_module_definitions(tmp_path: Path) -> None:
    module_root = tmp_path / "modules"
    nested = module_root / "sub"
    nested.mkdir(parents=True)

    module_definition = {
        "id": "nested-service",
        "name": "Nested Service",
        "version": "1.0.0",
        "schema_version": "1.0",
        "module_type": "service",
        "module_category": "feature",
    }
    (nested / "nested-service.json").write_text(json.dumps(module_definition, indent=2), encoding="utf-8")

    loader = ModuleLoader(module_root)
    modules = loader.discover_modules()

    assert len(modules) == 1
    assert modules[0].id == "nested-service"


def test_module_validator_detects_capability_integration_mismatch(tmp_path: Path) -> None:
    module_root = tmp_path / "modules"
    module_root.mkdir()

    module_definition = {
        "id": "bad-service",
        "name": "Bad Service",
        "version": "1.0.0",
        "schema_version": "1.0",
        "module_type": "service",
        "module_category": "feature",
        "capabilities": {"api": False},
        "api_integration": {"routes": ["/broken"]},
    }
    path = module_root / "bad-service.json"
    path.write_text(json.dumps(module_definition, indent=2), encoding="utf-8")

    loader = ModuleLoader(module_root)
    module = loader.load_module(path)

    from tools.generator.module_validator import ModuleValidator

    validator = ModuleValidator()
    errors = validator.validate(module)

    assert any("api_integration defined without api capability" in error for error in errors)


def test_cli_list_modules_supports_module_listing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    monkeypatch.chdir(project_root)

    project_definition = {
        "id": "cli-modules",
        "name": "CLI Modules Project",
        "version": "1.0.0",
        "schema_version": "1.0",
        "project_type": "application",
        "blueprint_root": "blueprints",
        "template_root": "templates",
        "module_root": "modules",
        "output_root": "output",
        "plugins": [],
    }
    project_path = project_root / ".rtiqa" / "project.json"
    project_path.parent.mkdir(parents=True, exist_ok=True)
    project_path.write_text(json.dumps(project_definition, indent=2), encoding="utf-8")

    (project_root / "blueprints").mkdir()
    (project_root / "templates").mkdir()
    (project_root / "modules").mkdir()
    (project_root / "output").mkdir()

    (project_root / "modules" / "cli-service.json").write_text(
        json.dumps(
            {
                "id": "cli-service",
                "name": "CLI Service",
                "version": "1.0.0",
                "schema_version": "1.0",
                "module_type": "service",
                "module_category": "feature",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    from tools.generator.cli import main

    exit_code = main(["--project-definition", str(project_path), "--list-modules"])

    assert exit_code == 0


def test_engine_raises_for_invalid_module_definition(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    project_definition = {
        "id": "invalid-module-project",
        "name": "Invalid Module Project",
        "version": "1.0.0",
        "schema_version": "1.0",
        "project_type": "application",
        "blueprint_root": "blueprints",
        "template_root": "templates",
        "module_root": "modules",
        "output_root": "output",
        "plugins": [],
    }

    project_path = project_root / ".rtiqa" / "project.json"
    project_path.parent.mkdir(parents=True, exist_ok=True)
    project_path.write_text(json.dumps(project_definition, indent=2), encoding="utf-8")

    blueprint_root = project_root / "blueprints"
    template_root = project_root / "templates"
    module_root = project_root / "modules"
    output_root = project_root / "output"
    blueprint_root.mkdir()
    template_root.mkdir()
    module_root.mkdir()
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

    module_definition = {
        "id": "broken-service",
        "name": "Broken Service",
        "version": "1.0.0",
        "schema_version": "1.0",
        "module_type": "service",
        "module_category": "feature",
        "capabilities": {"api": True},
    }
    (module_root / "broken-service.json").write_text(json.dumps(module_definition, indent=2), encoding="utf-8")

    with pytest.raises(ValueError, match="Module validation failed"):
        GeneratorEngine.from_project_definition(project_path)
