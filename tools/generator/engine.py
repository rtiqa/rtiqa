from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .blueprint_loader import BlueprintLoader
from .condition_evaluator import ConditionEvaluator
from .filesystem_writer import FilesystemWriter
from .models import Blueprint, FileArtifact, GenerationResult, ModuleDefinition, ProjectDefinition
from .module_loader import ModuleLoader
from .module_validator import ModuleValidator
from .project_loader import ProjectLoader
from .template_loader import TemplateLoader
from .validator import Validator

from packaging.version import InvalidVersion, Version

ENGINE_VERSION = "1.0.0"


class GeneratorEngine:
    """Core generator engine that coordinates blueprint loading, validation, rendering, and writing."""

    def __init__(
        self,
        blueprint_loader: BlueprintLoader,
        template_loader: TemplateLoader,
        validator: Validator,
        writer: FilesystemWriter,
        project_definition: Optional[ProjectDefinition] = None,
        module_loader: Optional[ModuleLoader] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.blueprint_loader = blueprint_loader
        self.template_loader = template_loader
        self.validator = validator
        self.writer = writer
        self.project_definition = project_definition
        self.module_loader = module_loader
        self.logger = logger or logging.getLogger(__name__)
        self._blueprints: Dict[str, Blueprint] = {}
        self._modules: Dict[str, ModuleDefinition] = {}
        self._module_validator = ModuleValidator()
        self.reload_blueprints()
        self.reload_modules()

    @classmethod
    def from_paths(
        cls,
        blueprint_root: Path,
        template_root: Path,
        output_root: Path,
        logger: Optional[logging.Logger] = None,
        module_root: Optional[Path] = None,
    ) -> "GeneratorEngine":
        shared_logger = logger or logging.getLogger(__name__)
        return cls(
            blueprint_loader=BlueprintLoader(blueprint_root),
            template_loader=TemplateLoader(template_root),
            validator=Validator(),
            writer=FilesystemWriter(output_root, logger=shared_logger),
            project_definition=None,
            module_loader=ModuleLoader(module_root) if module_root is not None else None,
            logger=shared_logger,
        )

    @classmethod
    def from_project_definition(
        cls,
        project_definition_path: Path,
        logger: Optional[logging.Logger] = None,
    ) -> "GeneratorEngine":
        project_definition = ProjectLoader(project_definition_path).load_project_definition()
        shared_logger = logger or logging.getLogger(__name__)
        blueprint_root = Path(project_definition.blueprint_root)
        template_root = Path(project_definition.template_root)
        module_root = Path(project_definition.module_root)
        output_root = Path(project_definition.output_root)

        return cls(
            blueprint_loader=BlueprintLoader(blueprint_root),
            template_loader=TemplateLoader(template_root),
            validator=Validator(),
            writer=FilesystemWriter(output_root, logger=shared_logger),
            project_definition=project_definition,
            logger=shared_logger,
            module_loader=ModuleLoader(module_root),
        )

    def reload_blueprints(self) -> None:
        self._blueprints = {
            blueprint.id: blueprint
            for blueprint in self.blueprint_loader.discover_blueprints()
        }
        self.logger.debug(
            "generator.blueprints.reload",
            extra={"blueprint_count": len(self._blueprints)},
        )

    def reload_modules(self) -> None:
        self._modules = {}
        loader = self.module_loader
        if loader is None and self.project_definition is not None:
            loader = ModuleLoader(Path(self.project_definition.module_root))

        if loader is None:
            return

        self._modules = {module.id: module for module in loader.discover_modules()}
        self._validate_modules()
        self._verify_module_dependencies()
        self.logger.debug(
            "generator.modules.reload",
            extra={"module_count": len(self._modules)},
        )

    def _validate_modules(self) -> None:
        errors: List[str] = []
        for module in self._modules.values():
            validation_errors = self._module_validator.validate(module)
            errors.extend([f"{module.id}: {message}" for message in validation_errors])
            errors.extend(self._validate_module_compatibility(module))

        if errors:
            raise ValueError(f"Module validation failed: {'; '.join(errors)}")

    def _validate_module_compatibility(self, module: ModuleDefinition) -> List[str]:
        errors: List[str] = []
        compatibility = module.compatibility
        engine_version = Version(ENGINE_VERSION)

        requires_engine = compatibility.get("engine")
        if requires_engine:
            try:
                if not self._matches_version(engine_version, requires_engine):
                    errors.append(
                        f"Module {module.id} requires engine {requires_engine}, current engine is {ENGINE_VERSION}."
                    )
            except ValueError as exc:
                errors.append(str(exc))

        requires_schema = compatibility.get("schema_version")
        if requires_schema:
            try:
                module_schema_version = Version(module.schema_version)
                if not self._matches_version(module_schema_version, requires_schema):
                    errors.append(
                        f"Module {module.id} requires schema version {requires_schema}, current schema version is {module.schema_version}."
                    )
            except ValueError as exc:
                errors.append(str(exc))

        return errors

    def _verify_module_dependencies(self) -> None:
        missing = [
            dep
            for module in self._modules.values()
            for dep in module.dependencies
            if dep not in self._modules
        ]
        if missing:
            raise ValueError(f"Module dependencies not found: {', '.join(sorted(set(missing)))}")

        graph = {module_id: module.dependencies for module_id, module in self._modules.items()}
        if cycle := self._detect_cycle(graph):
            raise ValueError(f"Module dependency cycle detected: {' -> '.join(cycle)}")

    def list_blueprints(self) -> List[Blueprint]:
        return list(self._blueprints.values())

    def list_modules(self) -> List[ModuleDefinition]:
        return list(self._modules.values())

    def generate(
        self,
        blueprint_name: str,
        inputs: Dict[str, Any],
        dry_run: bool = False,
        overwrite: bool = False,
    ) -> GenerationResult:
        self.logger.info(
            "generator.generate.request",
            extra={
                "blueprint": blueprint_name,
                "dry_run": dry_run,
                "overwrite": overwrite,
                "input_keys": list(inputs.keys()),
            },
        )

        blueprint = self._blueprints.get(blueprint_name)
        if blueprint is None:
            return GenerationResult(
                success=False,
                message=f"Blueprint not found: {blueprint_name}",
                errors=[f"Blueprint {blueprint_name} is unavailable."],
            )

        try:
            resolved_blueprint = self._resolve_blueprint(blueprint)
            self._verify_dependencies(resolved_blueprint)
            self._validate_compatibility(resolved_blueprint)
            self._validate_metadata_schema(resolved_blueprint)
        except Exception as exc:
            self.logger.error(
                "generator.resolve.failure",
                extra={"blueprint": blueprint_name, "error": str(exc)},
            )
            return GenerationResult(success=False, message="Blueprint resolution failed.", errors=[str(exc)])

        merged_inputs = {**resolved_blueprint.variables, **inputs}

        validation = self.validator.validate(resolved_blueprint.schema, merged_inputs)
        if not validation.valid:
            self.logger.warning(
                "generator.validate.failure",
                extra={"blueprint": blueprint_name, "errors": validation.errors},
            )
            return GenerationResult(success=False, message="Input validation failed.", errors=validation.errors)

        try:
            directories = self.writer.create_directories(resolved_blueprint.directories, dry_run=dry_run)
            file_entries = self._render_files(resolved_blueprint.files, merged_inputs, resolved_blueprint.template_map)
            written_files = self.writer.write_files(
                file_entries,
                dry_run=dry_run,
                overwrite=overwrite,
            )
        except Exception as exc:
            self.logger.error(
                "generator.generate.error",
                extra={"blueprint": blueprint_name, "error": str(exc)},
            )
            return GenerationResult(success=False, message="Generation failed.", errors=[str(exc)])

        message = "Dry run completed successfully." if dry_run else "Generation completed successfully."
        self.logger.info(
            "generator.generate.success",
            extra={
                "blueprint": blueprint_name,
                "generated_directories": [str(path) for path in directories],
                "generated_files": [str(path) for path in written_files],
                "dry_run": dry_run,
            },
        )
        return GenerationResult(
            success=True,
            message=message,
            generated_files=written_files,
            generated_directories=directories,
        )

    def _verify_dependencies(self, blueprint: Blueprint) -> None:
        missing = [name for name in blueprint.dependencies if name not in self._blueprints]
        if missing:
            raise ValueError(f"Blueprint dependencies not found: {', '.join(missing)}")

        graph = self._build_dependency_graph(blueprint)
        missing_references = self._find_missing_references(graph)
        if missing_references:
            raise ValueError(f"Blueprint references missing: {', '.join(sorted(missing_references))}")

        if cycle := self._detect_cycle(graph):
            raise ValueError(f"Dependency cycle detected: {' -> '.join(cycle)}")

    def _validate_compatibility(self, blueprint: Blueprint) -> None:
        compatibility = blueprint.compatibility
        engine_version = Version(ENGINE_VERSION)

        requires_engine = compatibility.get("engine")
        if requires_engine:
            if not self._matches_version(engine_version, requires_engine):
                raise ValueError(
                    f"Blueprint {blueprint.id} requires engine {requires_engine}, current engine is {ENGINE_VERSION}."
                )

        requires_schema = compatibility.get("schema_version")
        if requires_schema:
            blueprint_schema_version = Version(blueprint.schema_version)
            if not self._matches_version(blueprint_schema_version, requires_schema):
                raise ValueError(
                    f"Blueprint {blueprint.id} requires schema version {requires_schema}, current schema version is {blueprint.schema_version}."
                )

    def _validate_metadata_schema(self, blueprint: Blueprint) -> None:
        if not blueprint.metadata_schema:
            return

        validation = self.validator.validate(blueprint.metadata_schema, blueprint.metadata)
        if not validation.valid:
            raise ValueError(
                f"Blueprint {blueprint.id} metadata schema validation failed: {'; '.join(validation.errors)}"
            )

    def _matches_version(self, version: Version, requirement: str) -> bool:
        try:
            if requirement.startswith("^"):
                base = Version(requirement[1:])
                return version >= base and version < Version(f"{base.major + 1}.0.0")
            if requirement.startswith("~"):
                base = Version(requirement[1:])
                return version >= base and version < Version(f"{base.major}.{base.minor + 1}.0")
            return version == Version(requirement)
        except InvalidVersion:
            raise ValueError(f"Invalid compatibility version expression: {requirement}")

    def _build_dependency_graph(self, blueprint: Blueprint) -> Dict[str, List[str]]:
        graph: Dict[str, List[str]] = {}

        def visit(node: Blueprint) -> None:
            if node.id in graph:
                return
            references = [*node.extends, *node.compose, *node.dependencies]
            graph[node.id] = references
            for ref in references:
                if ref in self._blueprints:
                    visit(self._blueprints[ref])
                else:
                    graph.setdefault(node.id, references)

        visit(blueprint)
        return graph

    def _detect_cycle(self, graph: Dict[str, List[str]]) -> List[str]:
        visited = set()
        stack = []

        def dfs(node: str) -> List[str]:
            if node in stack:
                return stack[stack.index(node):] + [node]
            if node in visited:
                return []
            visited.add(node)
            stack.append(node)
            for neighbor in graph.get(node, []):
                cycle = dfs(neighbor)
                if cycle:
                    return cycle
            stack.pop()
            return []

        for node in graph:
            if cycle := dfs(node):
                return cycle
        return []

    def _find_missing_references(self, graph: Dict[str, List[str]]) -> List[str]:
        missing = []
        for refs in graph.values():
            for reference in refs:
                if reference not in self._blueprints and reference not in missing:
                    missing.append(reference)
        return missing

    def _resolve_blueprint(self, blueprint: Blueprint, visited: Optional[set[str]] = None) -> Blueprint:
        if visited is None:
            visited = set()

        if blueprint.id in visited:
            raise ValueError(f"Circular blueprint reference detected: {' -> '.join(list(visited) + [blueprint.id])}")
        visited.add(blueprint.id)

        if not blueprint.extends and not blueprint.compose:
            return blueprint

        combined = Blueprint(
            id=blueprint.id,
            name=blueprint.name,
            description=blueprint.description,
            version=blueprint.version,
            schema_version=blueprint.schema_version,
            metadata={**blueprint.metadata},
            metadata_schema={**blueprint.metadata_schema},
            compatibility={**blueprint.compatibility},
            category=blueprint.category,
            outputs={**blueprint.outputs},
            schema={**blueprint.schema},
            variables={**blueprint.variables},
            conditions=[*blueprint.conditions],
            dependencies=[*blueprint.dependencies],
            extends=[*blueprint.extends],
            compose=[*blueprint.compose],
            template_map={**blueprint.template_map},
            directories=[*blueprint.directories],
            files=[*blueprint.files],
        )

        for source_name in [*blueprint.extends, *blueprint.compose]:
            source = self._blueprints.get(source_name)
            if source is None:
                raise ValueError(f"Referenced blueprint not found: {source_name}")
            resolved_source = self._resolve_blueprint(source, set(visited))
            combined = self._merge_blueprints(resolved_source, combined)

        return combined

    def _merge_blueprints(self, base: Blueprint, overlay: Blueprint) -> Blueprint:
        merged_schema = self._merge_schema(base.schema, overlay.schema)
        merged_variables = {**base.variables, **overlay.variables}
        merged_template_map = {**base.template_map, **overlay.template_map}
        merged_directories = [*base.directories]
        for directory in overlay.directories:
            if directory not in merged_directories:
                merged_directories.append(directory)

        merged_files: List[FileArtifact] = [*base.files]
        existing_paths = {item.path for item in merged_files}
        for item in overlay.files:
            if item.path in existing_paths:
                merged_files = [item if existing.path == item.path else existing for existing in merged_files]
            else:
                merged_files.append(item)

        merged_metadata = self._deep_merge_metadata(base.metadata, overlay.metadata)
        merged_compatibility = {**base.compatibility, **overlay.compatibility}

        return Blueprint(
            id=overlay.id,
            name=overlay.name,
            description=overlay.description or base.description,
            version=overlay.version,
            schema_version=overlay.schema_version,
            metadata=merged_metadata,
            metadata_schema={**base.metadata_schema, **overlay.metadata_schema},
            compatibility=merged_compatibility,
            category=overlay.category or base.category,
            outputs={**base.outputs, **overlay.outputs},
            schema=merged_schema,
            variables=merged_variables,
            conditions=[*base.conditions, *overlay.conditions],
            dependencies=[*base.dependencies, *overlay.dependencies],
            extends=[*base.extends, *overlay.extends],
            compose=[*base.compose, *overlay.compose],
            template_map=merged_template_map,
            directories=merged_directories,
            files=merged_files,
        )

    def _merge_schema(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        merged: Dict[str, Any] = {**base}
        if not overlay:
            return merged

        def deep_merge(base_value: Any, overlay_value: Any) -> Any:
            if isinstance(base_value, dict) and isinstance(overlay_value, dict):
                merged_value = {**base_value}
                for key, value in overlay_value.items():
                    merged_value[key] = deep_merge(merged_value.get(key), value) if key in merged_value else value
                return merged_value
            return overlay_value

        for section in ["required", "optional"]:
            base_section = base.get(section, {})
            overlay_section = overlay.get(section, {})
            if isinstance(base_section, dict) and isinstance(overlay_section, dict):
                merged[section] = deep_merge(base_section, overlay_section)
            else:
                merged[section] = overlay_section

        return merged

    def _deep_merge_metadata(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        merged: Dict[str, Any] = {**base}
        for key, value in overlay.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._deep_merge_metadata(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _render_files(
        self,
        files: List[FileArtifact],
        inputs: Dict[str, Any],
        template_map: Dict[str, str],
    ) -> List[tuple[str, str]]:
        rendered: List[tuple[str, str]] = []
        for item in files:
            if not self._should_render(item.condition, inputs):
                self.logger.debug(
                    "generator.file.skip",
                    extra={"path": item.path, "condition": item.condition},
                )
                continue

            template_name = template_map.get(item.template_name, item.template_name)
            content = self.template_loader.render(template_name, {**inputs, **item.variables})
            self.logger.debug(
                "generator.template.render",
                extra={"template": template_name, "path": item.path},
            )
            rendered.append((item.path, content))
        return rendered

    def _should_render(self, condition: Optional[str], context: Dict[str, Any]) -> bool:
        if not condition:
            return True
        return ConditionEvaluator().evaluate(condition, context)
