from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from .models import MODULE_CAPABILITIES, MODULE_LIFECYCLE_STAGES, MODULE_TYPES, MODULE_CATEGORIES, ModuleDefinition


class ModuleValidator:
    """Validate RTIQA module definitions and dependency rules."""

    def validate(self, module: ModuleDefinition) -> List[str]:
        errors: List[str] = []

        if module.module_type not in MODULE_TYPES:
            errors.append(f"Invalid module_type: {module.module_type}")

        if module.module_category not in MODULE_CATEGORIES:
            errors.append(f"Invalid module_category: {module.module_category}")

        stage = module.lifecycle.get("stage")
        if stage is not None and stage not in MODULE_LIFECYCLE_STAGES:
            errors.append(f"Invalid lifecycle.stage: {stage}")

        if not isinstance(module.capabilities, dict):
            errors.append("capabilities must be an object.")
        else:
            for capability, value in module.capabilities.items():
                if capability not in MODULE_CAPABILITIES:
                    errors.append(f"Unsupported capability: {capability}")
                    continue

                if not isinstance(value, (bool, dict)):
                    errors.append(f"Capability {capability} must be a boolean or an object.")

                if capability == "database" and value is not False and not module.database_integration:
                    errors.append("Database capability declared without database_integration details.")
                if capability == "api" and value is not False and not module.api_integration:
                    errors.append("API capability declared without api_integration details.")
                if capability == "ui" and value is not False and not module.ui_integration:
                    errors.append("UI capability declared without ui_integration details.")
                if capability == "ai" and value is not False and not module.ai_integration:
                    errors.append("AI capability declared without ai_integration details.")
                if capability == "service" and value is not False and not module.service_integration:
                    errors.append("Service capability declared without service_integration details.")

        if module.api_integration and module.capabilities.get("api") is False:
            errors.append("api_integration defined without api capability.")
        if module.database_integration and module.capabilities.get("database") is False:
            errors.append("database_integration defined without database capability.")
        if module.ui_integration and module.capabilities.get("ui") is False:
            errors.append("ui_integration defined without ui capability.")
        if module.ai_integration and module.capabilities.get("ai") is False:
            errors.append("ai_integration defined without ai capability.")
        if module.service_integration and module.capabilities.get("service") is False:
            errors.append("service_integration defined without service capability.")

        if module.permissions and not isinstance(module.permissions, dict):
            errors.append("permissions must be an object.")
        elif isinstance(module.permissions, dict):
            for key, value in module.permissions.items():
                if not isinstance(key, str):
                    errors.append("permissions keys must be strings.")
                if not isinstance(value, (bool, dict, list)):
                    errors.append("permissions values must be boolean, object, or list.")

        if module.events and not isinstance(module.events, dict):
            errors.append("events must be an object.")
        elif isinstance(module.events, dict):
            for key, value in module.events.items():
                if not isinstance(key, str):
                    errors.append("events keys must be strings.")
                if not isinstance(value, dict):
                    errors.append("events values must be objects.")

        if module.id in module.dependencies:
            errors.append("Module cannot depend on itself.")

        duplicate_dependencies = self._find_duplicate_dependencies(module.dependencies)
        if duplicate_dependencies:
            errors.append(f"Duplicate module dependencies: {', '.join(sorted(duplicate_dependencies))}")

        return errors

    def _find_duplicate_dependencies(self, dependencies: List[str]) -> List[str]:
        seen = set()
        duplicates: List[str] = []
        for dependency in dependencies:
            if dependency in seen and dependency not in duplicates:
                duplicates.append(dependency)
            seen.add(dependency)
        return duplicates
