from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class FileArtifact:
    path: str
    template_name: str
    variables: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Blueprint:
    name: str
    description: str
    schema: Dict[str, Any]
    directories: List[str] = field(default_factory=list)
    files: List[FileArtifact] = field(default_factory=list)


@dataclass
class ValidationResult:
    valid: bool
    errors: List[str] = field(default_factory=list)


@dataclass
class GenerationResult:
    success: bool
    message: str
    generated_files: List[Path] = field(default_factory=list)
    generated_directories: List[Path] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
