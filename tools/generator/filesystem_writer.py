from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, List, Optional


class FilesystemWriter:
    """Write directories and rendered files to disk."""

    def __init__(self, root: Path, logger: Optional[logging.Logger] = None) -> None:
        self.root = root
        self.logger = logger or logging.getLogger(__name__)

    def _resolve_path(self, relative_path: str) -> Path:
        path = Path(relative_path)
        if path.is_absolute():
            raise ValueError("Absolute paths are not allowed for generation output.")

        resolved = (self.root / path).resolve()
        root_resolved = self.root.resolve()
        if root_resolved not in resolved.parents and root_resolved != resolved:
            raise ValueError("Output path escapes the configured root.")

        return resolved

    def create_directories(self, directories: Iterable[str], dry_run: bool = False) -> List[Path]:
        created: List[Path] = []
        for directory in directories:
            resolved_path = self._resolve_path(directory)
            self.logger.debug(
                "generator.filesystem.create_directory",
                extra={"path": str(resolved_path), "dry_run": dry_run},
            )
            if not dry_run:
                resolved_path.mkdir(parents=True, exist_ok=True)
            created.append(resolved_path)
        return created

    def write_files(
        self,
        files: Iterable[tuple[str, str]],
        dry_run: bool = False,
        overwrite: bool = False,
    ) -> List[Path]:
        written: List[Path] = []
        for relative_path, content in files:
            resolved_path = self._resolve_path(relative_path)
            self.logger.debug(
                "generator.filesystem.write_file",
                extra={
                    "path": str(resolved_path),
                    "dry_run": dry_run,
                    "overwrite": overwrite,
                },
            )
            if resolved_path.exists() and not overwrite:
                raise FileExistsError(f"File already exists and overwrite is disabled: {resolved_path}")

            if dry_run:
                written.append(resolved_path)
                continue

            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            resolved_path.write_text(content, encoding="utf-8")
            written.append(resolved_path)
        return written
