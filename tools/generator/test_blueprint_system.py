from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict

import pytest

from tools.generator.blueprint_loader import BlueprintLoader
from tools.generator.engine import GeneratorEngine
from tools.generator.models import Blueprint
from tools.generator.validator import Validator


@pytest.fixture
def temporary_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "generator_test"
    root.mkdir()
    monkeypatch.chdir(root)
    return root


def write_blueprint(root: Path, name: str, payload: Dict[str, Any]) -> Path:
    path = root / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_template(root: Path, name: str, content: str) -> Path:
    path = root / name
    path.write_text(content, encoding="utf-8")
    return path


def test_blueprint_inheritance_and_variable_inheritance(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "base.tpl", "Base {project_name}\n")
    write_template(templates, "child.tpl", "Child {project_name} - {team}\n")

    write_blueprint(
        blueprints,
        "base",
        {
            "id": "base",
            "name": "Base Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "schema": {"required": {"project_name": "string"}},
            "variables": {"team": "core"},
            "files": [{"path": "base.txt", "template": "base.tpl"}],
        },
    )

    write_blueprint(
        blueprints,
        "child",
        {
            "id": "child",
            "name": "Child Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "extends": ["base"],
            "schema": {"required": {"project_name": "string"}},
            "files": [
                {
                    "path": "child.txt",
                    "template": "child.tpl",
                    "variables": {"team": "child-team"},
                }
            ],
        },
    )

    engine = GeneratorEngine.from_paths(blueprints, templates, output)
    result = engine.generate("child", {"project_name": "Demo"}, dry_run=True)

    assert result.success
    assert output.joinpath("base.txt") in result.generated_files
    assert output.joinpath("child.txt") in result.generated_files


def test_blueprint_composition_and_template_mapping(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "base.tpl", "Base {project_name}\n")
    write_template(templates, "alternate.tpl", "Alternate {project_name}\n")

    write_blueprint(
        blueprints,
        "core",
        {
            "id": "core",
            "name": "Core Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "core.txt", "template": "base.tpl"}],
        },
    )

    write_blueprint(
        blueprints,
        "composed",
        {
            "id": "composed",
            "name": "Composed Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "compose": ["core"],
            "template_map": {"base.tpl": "alternate.tpl"},
            "files": [{"path": "core.txt", "template": "base.tpl"}],
        },
    )

    engine = GeneratorEngine.from_paths(blueprints, templates, output)
    result = engine.generate("composed", {"project_name": "Demo"}, dry_run=True)

    assert result.success
    assert output.joinpath("core.txt") in result.generated_files


def test_dependency_resolution(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "dep.tpl", "Dep {project_name}\n")

    write_blueprint(
        blueprints,
        "dep",
        {
            "id": "dep",
            "name": "Dependency Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "dep.txt", "template": "dep.tpl"}],
        },
    )

    write_blueprint(
        blueprints,
        "dependent",
        {
            "id": "dependent",
            "name": "Dependent Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "dependencies": ["dep"],
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "dependent.txt", "template": "dep.tpl"}],
        },
    )

    engine = GeneratorEngine.from_paths(blueprints, templates, output)
    result = engine.generate("dependent", {"project_name": "Demo"}, dry_run=True)

    assert result.success


def test_circular_dependency_detection(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "loop.tpl", "Loop {project_name}\n")

    write_blueprint(
        blueprints,
        "a",
        {
            "id": "a",
            "name": "Blueprint A",
            "version": "1.0.0",
            "schema_version": "1.0",
            "extends": ["b"],
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "a.txt", "template": "loop.tpl"}],
        },
    )

    write_blueprint(
        blueprints,
        "b",
        {
            "id": "b",
            "name": "Blueprint B",
            "version": "1.0.0",
            "extends": ["a"],
            "schema_version": "1.0",
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "b.txt", "template": "loop.tpl"}],
        },
    )

    engine = GeneratorEngine.from_paths(blueprints, templates, output)
    result = engine.generate("a", {"project_name": "Demo"}, dry_run=True)

    assert not result.success
    assert "Circular blueprint reference" in result.errors[0]


def test_conditional_rendering(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "cond.tpl", "Cond {project_name}\n")

    write_blueprint(
        blueprints,
        "conditional",
        {
            "id": "conditional",
            "name": "Conditional Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "schema": {"required": {"project_name": "string", "render": "boolean"}},
            "files": [
                {
                    "path": "when_true.txt",
                    "template": "cond.tpl",
                    "condition": "render == True",
                }
            ],
        },
    )

    engine = GeneratorEngine.from_paths(blueprints, templates, output)
    result_false = engine.generate("conditional", {"project_name": "Demo", "render": False}, dry_run=True)
    result_true = engine.generate("conditional", {"project_name": "Demo", "render": True}, dry_run=True)

    assert result_false.success
    assert output.joinpath("when_true.txt") not in result_false.generated_files
    assert result_true.success
    assert output.joinpath("when_true.txt") in result_true.generated_files


def test_schema_validation_failure(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "fail.tpl", "Fail {project_name}\n")

    write_blueprint(
        blueprints,
        "schema_fail",
        {
            "id": "schema_fail",
            "name": "Schema Fail Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "schema": {"required": {"project_name": "string", "version": "integer"}},
            "files": [{"path": "fail.txt", "template": "fail.tpl"}],
        },
    )

    engine = GeneratorEngine.from_paths(blueprints, templates, output)
    result = engine.generate("schema_fail", {"project_name": "Demo"}, dry_run=True)

    assert not result.success
    assert any("Missing required input" in error for error in result.errors)


def test_metadata_schema_validation_failure(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "meta.tpl", "Meta {project_name}\n")

    write_blueprint(
        blueprints,
        "meta_fail",
        {
            "id": "meta_fail",
            "name": "Metadata Fail Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "metadata": {"owner": "team-a", "labels": {"env": "prod"}},
            "metadata_schema": {
                "required": {"owner": "string", "labels": {"required": {"env": "integer"}}}
            },
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "meta.txt", "template": "meta.tpl"}],
        },
    )

    engine = GeneratorEngine.from_paths(blueprints, templates, output)
    result = engine.generate("meta_fail", {"project_name": "Demo"}, dry_run=True)

    assert not result.success
    assert any("metadata schema validation" in error for error in result.errors)


def test_compatibility_engine_version_mismatch(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "compat.tpl", "Compat {project_name}\n")

    write_blueprint(
        blueprints,
        "compat_fail",
        {
            "id": "compat_fail",
            "name": "Compatibility Fail Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "compatibility": {"engine": "^2.0.0"},
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "compat.txt", "template": "compat.tpl"}],
        },
    )

    engine = GeneratorEngine.from_paths(blueprints, templates, output)
    result = engine.generate("compat_fail", {"project_name": "Demo"}, dry_run=True)

    assert not result.success
    assert any("requires engine" in error for error in result.errors)


def test_compatibility_schema_version_mismatch(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "schema_compat.tpl", "SchemaCompat {project_name}\n")

    write_blueprint(
        blueprints,
        "schema_compat_fail",
        {
            "id": "schema_compat_fail",
            "name": "Schema Compatibility Fail Blueprint",
            "version": "1.0.0",
            "schema_version": "2.0",
            "compatibility": {"schema_version": "~1.0"},
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "schema_compat.txt", "template": "schema_compat.tpl"}],
        },
    )

    engine = GeneratorEngine.from_paths(blueprints, templates, output)
    result = engine.generate("schema_compat_fail", {"project_name": "Demo"}, dry_run=True)

    assert not result.success
    assert any("requires schema version" in error for error in result.errors)


def test_version_validation_failure(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    templates = temporary_environment / "templates"
    output = temporary_environment / "output"
    blueprints.mkdir()
    templates.mkdir()
    output.mkdir()

    write_template(templates, "v.tpl", "Version {project_name}\n")

    write_blueprint(
        blueprints,
        "bad_version",
        {
            "id": "bad_version",
            "name": "Bad Version Blueprint",
            "version": "not-a-version",
            "schema_version": "1.0",
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "bad.txt", "template": "v.tpl"}],
        },
    )

    loader = BlueprintLoader(blueprints)
    with pytest.raises(ValueError, match="semantic version format"):
        loader.discover_blueprints()


def test_invalid_metadata(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    blueprints.mkdir()
    write_blueprint(
        blueprints,
        "bad_meta",
        {
            "id": "bad_meta",
            "name": "Bad Metadata Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "metadata": ["not-an-object"],
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "meta.txt", "template": "v.tpl"}],
        },
    )

    loader = BlueprintLoader(blueprints)
    with pytest.raises(ValueError, match="field metadata must be an object"):
        loader.discover_blueprints()


def test_missing_required_fields(temporary_environment: Path):
    blueprints = temporary_environment / "blueprints"
    blueprints.mkdir()
    write_blueprint(
        blueprints,
        "missing_id",
        {
            "name": "Missing ID Blueprint",
            "version": "1.0.0",
            "schema_version": "1.0",
            "schema": {"required": {"project_name": "string"}},
            "files": [{"path": "missing.txt", "template": "v.tpl"}],
        },
    )

    loader = BlueprintLoader(blueprints)
    with pytest.raises(ValueError, match="must include a non-empty string id"):
        loader.discover_blueprints()
