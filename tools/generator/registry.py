from __future__ import annotations

import importlib.util
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional


class GeneratorPlugin(ABC):
    """Base class for generator plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def register(self) -> Dict[str, str]:
        raise NotImplementedError


class GeneratorRegistry:
    """Discover and manage registered generator plugins."""

    def __init__(self) -> None:
        self._registry: Dict[str, GeneratorPlugin] = {}

    def register(self, plugin: GeneratorPlugin) -> None:
        metadata = plugin.register()
        plugin_name = metadata.get("name")
        if not plugin_name:
            raise ValueError("Plugin metadata must include a name.")

        if plugin_name in self._registry:
            raise ValueError(f"Generator already registered: {plugin_name}")

        self._registry[plugin_name] = plugin

    def get(self, name: str) -> Optional[GeneratorPlugin]:
        return self._registry.get(name)

    def all(self) -> List[GeneratorPlugin]:
        return list(self._registry.values())

    def load_from_directory(self, path: Path) -> None:
        if not path.exists():
            return

        for file_path in sorted(path.glob("*.py")):
            if file_path.name == "__init__.py":
                continue

            spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
            if spec is None or spec.loader is None:
                continue

            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            try:
                spec.loader.exec_module(module)
            except Exception as exc:
                raise ImportError(f"Cannot import plugin from {file_path}: {exc}") from exc

            plugin = getattr(module, "plugin", None)
            if plugin is None:
                continue

            if not isinstance(plugin, GeneratorPlugin):
                raise TypeError(f"Plugin object in {file_path} must be a GeneratorPlugin instance.")

            self.register(plugin)
