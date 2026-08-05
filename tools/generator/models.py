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


PROJECT_TYPES = {
    "application",
    "service",
    "library",
    "integration",
    "platform",
    "infrastructure",
}

PROJECT_LIFECYCLE_STAGES = {
    "concept",
    "planning",
    "development",
    "staging",
    "production",
    "maintenance",
    "retirement",
}

MODULE_TYPES = {
    "domain",
    "service",
    "integration",
    "utility",
    "data",
    "ui",
    "ai",
    "security",
    "infrastructure",
}

MODULE_CATEGORIES = {
    "core",
    "shared",
    "feature",
    "integration",
    "platform",
    "extension",
    "experimental",
}

MODULE_CAPABILITIES = {
    "api",
    "database",
    "ui",
    "ai",
    "service",
    "security",
    "data",
    "integration",
}

MODULE_LIFECYCLE_STAGES = {
    "definition",
    "design",
    "development",
    "testing",
    "deployment",
    "maintenance",
    "deprecated",
    "retirement",
}


@dataclass
class PluginDefinition:
    id: str
    name: str
    version: str
    entrypoint: str
    enabled: bool = True
    description: str = ""
    configuration_schema: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectDefinition:
    id: str
    name: str
    description: str
    version: str
    schema_version: str
    project_type: str
    application_boundary: Dict[str, Any] = field(default_factory=dict)
    module_categories: List[str] = field(default_factory=list)
    service_categories: List[str] = field(default_factory=list)
    infrastructure_categories: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    lifecycle: Dict[str, Any] = field(default_factory=dict)
    extensions: Dict[str, Any] = field(default_factory=dict)
    blueprint_root: Path = Path(".rtiqa/blueprints")
    template_root: Path = Path(".rtiqa/templates")
    module_root: Path = Path(".rtiqa/modules")
    output_root: Path = Path(".")
    plugins: List[PluginDefinition] = field(default_factory=list)


@dataclass
class ModuleDefinition:
    id: str
    name: str
    description: str
    version: str
    schema_version: str
    module_type: str
    module_category: str
    module_categories: List[str] = field(default_factory=list)
    module_tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    lifecycle: Dict[str, Any] = field(default_factory=dict)
    capabilities: Dict[str, Any] = field(default_factory=dict)
    service_integration: Dict[str, Any] = field(default_factory=dict)
    api_integration: Dict[str, Any] = field(default_factory=dict)
    database_integration: Dict[str, Any] = field(default_factory=dict)
    ui_integration: Dict[str, Any] = field(default_factory=dict)
    ai_integration: Dict[str, Any] = field(default_factory=dict)
    permissions: Dict[str, Any] = field(default_factory=dict)
    events: Dict[str, Any] = field(default_factory=dict)
    extensions: Dict[str, Any] = field(default_factory=dict)
    compatibility: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)


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
