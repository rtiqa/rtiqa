from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from .engine import GeneratorEngine


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        extra_keys = [
            key
            for key in record.__dict__
            if key not in logging.LogRecord(None, None, None, None, None, None, None).__dict__
            and key not in {"args", "message"}
        ]

        for key in extra_keys:
            value = record.__dict__[key]
            try:
                json.dumps(value)
                payload[key] = value
            except TypeError:
                payload[key] = str(value)

        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("rtiqa.generator")
    logger.setLevel(level.upper())

    handler = logging.StreamHandler(sys.stderr)
    formatter = JsonLogFormatter()
    handler.setFormatter(formatter)
    handler.setLevel(level.upper())

    logger.handlers[:] = [handler]
    logger.propagate = False

    return logger


def parse_inputs(input_string: Optional[str], input_file: Optional[str]) -> Dict[str, Any]:
    if input_string and input_file:
        raise ValueError("Specify exactly one of --inputs or --inputs-file.")

    raw_value: Optional[str] = None
    if input_file:
        raw_path = Path(input_file)
        if not raw_path.exists():
            raise ValueError(f"Input file not found: {input_file}")
        raw_value = raw_path.read_text(encoding="utf-8")
    elif input_string:
        raw_value = input_string

    if not raw_value:
        return {}

    try:
        parsed = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON input: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Input payload must be a JSON object.")

    return parsed


def format_blueprints(blueprints: Iterable[Any]) -> str:
    lines: list[str] = []
    for item in blueprints:
        description = getattr(item, "description", "")
        category = getattr(item, "category", "")
        lines.append(f"- {item.id} ({item.name}) [{category}]: {description}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="RTIQA Project Generator CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--project-definition", default=".rtiqa/project.json", help="Path to the RTIQA project definition file.")
    parser.add_argument("--blueprint-root", default=".rtiqa/blueprints", help="Path to blueprint definitions.")
    parser.add_argument("--template-root", default=".rtiqa/templates", help="Path to template files.")
    parser.add_argument("--output-root", default=".", help="Project output root directory.")
    parser.add_argument("--blueprint", help="ID of the blueprint to execute.")
    parser.add_argument("--inputs", help="JSON payload to provide as blueprint inputs.")
    parser.add_argument("--inputs-file", help="Path to a JSON file containing blueprint inputs.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and render output without writing files.")
    parser.add_argument("--overwrite", action="store_true", help="Allow overwriting existing files during generation.")
    parser.add_argument("--list", action="store_true", help="List available blueprints and exit.")
    parser.add_argument("--log-level", default="INFO", help="Logging level for generator execution.")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logger = configure_logging(args.log_level)
    logger.debug(
        "generator.cli.start",
        extra={"parsed_args": vars(args)},
    )

    project_definition_path = Path(args.project_definition)
    blueprint_root = Path(args.blueprint_root)
    template_root = Path(args.template_root)
    output_root = Path(args.output_root)

    if project_definition_path.exists():
        engine = GeneratorEngine.from_project_definition(project_definition_path, logger=logger)
    else:
        engine = GeneratorEngine.from_paths(blueprint_root, template_root, output_root, logger=logger)

    if args.list:
        blueprints = engine.list_blueprints()
        if not blueprints:
            logger.info("generator.cli.no_blueprints", extra={"blueprint_root": str(blueprint_root)})
            print("No blueprints found.")
            return 0

        print(format_blueprints(blueprints))
        return 0

    if not args.blueprint:
        parser.error("A blueprint id is required unless --list is provided.")

    try:
        inputs = parse_inputs(args.inputs, args.inputs_file)
    except ValueError as exc:
        logger.error("generator.cli.invalid_inputs", extra={"error": str(exc)})
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    result = engine.generate(
        args.blueprint,
        inputs,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
    )

    if not result.success:
        logger.error(
            "generator.cli.failure",
            extra={"blueprint": args.blueprint, "errors": result.errors},
        )
        print("Generation failed:", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    logger.info(
        "generator.cli.success",
        extra={
            "blueprint": args.blueprint,
            "generated_directories": [str(path) for path in result.generated_directories],
            "generated_files": [str(path) for path in result.generated_files],
            "dry_run": args.dry_run,
        },
    )
    print(result.message)
    if result.generated_directories:
        print("Directories:")
        for path in result.generated_directories:
            print(f"- {path}")
    if result.generated_files:
        print("Files:")
        for path in result.generated_files:
            print(f"- {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
