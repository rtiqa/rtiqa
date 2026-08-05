from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class FileArtifact:
    path: str
    template_name: str
    variables: Dict[str, Any] = field(default_factory=dict)
    condition: Optional[str] = None


@dataclass
class Blueprint:
    id: str
    name: str
    description: str
    version: str
    schema_version: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    category: str = ""
    outputs: Dict[str, Any] = field(default_factory=dict)
    metadata_schema: Dict[str, Any] = field(default_factory=dict)
    compatibility: Dict[str, Any] = field(default_factory=dict)
    schema: Dict[str, Any] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    extends: List[str] = field(default_factory=list)
    compose: List[str] = field(default_factory=list)
    template_map: Dict[str, str] = field(default_factory=dict)
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
