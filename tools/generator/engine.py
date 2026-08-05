from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .blueprint_loader import BlueprintLoader
from .filesystem_writer import FilesystemWriter
from .models import Blueprint, FileArtifact, GenerationResult
from .template_loader import TemplateLoader
from .validator import Validator


class GeneratorEngine:
    """Core generator engine that coordinates blueprint loading, validation, rendering, and writing."""

    def __init__(
        self,
        blueprint_loader: BlueprintLoader,
        template_loader: TemplateLoader,
        validator: Validator,
        writer: FilesystemWriter,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.blueprint_loader = blueprint_loader
        self.template_loader = template_loader
        self.validator = validator
        self.writer = writer
        self.logger = logger or logging.getLogger(__name__)
        self._blueprints: Dict[str, Blueprint] = {}
        self.reload_blueprints()

    @classmethod
    def from_paths(
        cls,
        blueprint_root: Path,
        template_root: Path,
        output_root: Path,
        logger: Optional[logging.Logger] = None,
    ) -> "GeneratorEngine":
        shared_logger = logger or logging.getLogger(__name__)
        return cls(
            blueprint_loader=BlueprintLoader(blueprint_root),
            template_loader=TemplateLoader(template_root),
            validator=Validator(),
            writer=FilesystemWriter(output_root, logger=shared_logger),
            logger=shared_logger,
        )

    def reload_blueprints(self) -> None:
        self._blueprints = {
            blueprint.name: blueprint
            for blueprint in self.blueprint_loader.discover_blueprints()
        }
        self.logger.debug(
            "generator.blueprints.reload",
            extra={"blueprint_count": len(self._blueprints)},
        )

    def list_blueprints(self) -> List[Blueprint]:
        return list(self._blueprints.values())

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

        validation = self.validator.validate(blueprint.schema, inputs)
        if not validation.valid:
            self.logger.warning(
                "generator.validate.failure",
                extra={"blueprint": blueprint_name, "errors": validation.errors},
            )
            return GenerationResult(success=False, message="Input validation failed.", errors=validation.errors)

        try:
            directories = self.writer.create_directories(blueprint.directories, dry_run=dry_run)
            file_entries = self._render_files(blueprint.files, inputs)
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

    def _render_files(self, files: List[FileArtifact], inputs: Dict[str, Any]) -> List[tuple[str, str]]:
        rendered: List[tuple[str, str]] = []
        for item in files:
            content = self.template_loader.render(item.template_name, {**inputs, **item.variables})
            self.logger.debug(
                "generator.template.render",
                extra={"template": item.template_name, "path": item.path},
            )
            rendered.append((item.path, content))
        return rendered
