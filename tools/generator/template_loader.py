from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


class TemplateLoader:
    """Load and render templates for the generator engine."""

    def __init__(self, template_root: Path) -> None:
        self.template_root = template_root

    def _resolve_template_path(self, template_name: str) -> Path:
        path = Path(template_name)
        if path.is_absolute():
            raise ValueError("Absolute template paths are not allowed.")

        resolved = (self.template_root / path).resolve()
        root_resolved = self.template_root.resolve()
        if root_resolved not in resolved.parents and root_resolved != resolved:
            raise ValueError("Template path escapes the template root.")

        return resolved

    def load_template(self, template_name: str) -> str:
        path = self._resolve_template_path(template_name)
        if not path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")

        return path.read_text(encoding="utf-8")

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        content = self.load_template(template_name)
        try:
            return content.format_map(StrictFormatDict(context))
        except KeyError as exc:
            raise ValueError(f"Missing template variable: {exc}") from exc


class StrictFormatDict(dict):
    def __missing__(self, key: str) -> str:
        raise KeyError(f"Missing template variable: {key}")
