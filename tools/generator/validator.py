from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict

from .models import ValidationResult

SEMVER_PATTERN = r"^\d+\.\d+(?:\.\d+)?(?:[-+][0-9A-Za-z.-]+)?$"


def validate_semantic_version(value: str, field: str, path: Path) -> str:
    if not isinstance(value, str) or not re.match(SEMVER_PATTERN, value):
        raise ValueError(f"{path} field {field} must follow semantic version format.")
    return value


class Validator:
    """Validate input payloads against blueprint schemas."""

    VALID_TYPES = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "object": dict,
        "array": list,
    }

    def validate(self, schema: Dict[str, Any], data: Dict[str, Any]) -> ValidationResult:
        if not isinstance(schema, dict):
            return ValidationResult(valid=False, errors=["Schema must be an object."])

        if not isinstance(data, dict):
            return ValidationResult(valid=False, errors=["Input data must be an object."])

        errors: List[str] = []
        required = schema.get("required", {})
        optional = schema.get("optional", {})

        if not isinstance(required, dict):
            return ValidationResult(valid=False, errors=["Schema `required` section must be an object."])

        if not isinstance(optional, dict):
            return ValidationResult(valid=False, errors=["Schema `optional` section must be an object."])

        for key, expected_type in required.items():
            if key not in data:
                errors.append(f"Missing required input: {key}")
                continue

            self._validate_type(key, expected_type, data.get(key), errors)

        for key, expected_type in optional.items():
            if key in data:
                self._validate_type(key, expected_type, data.get(key), errors)

        return ValidationResult(valid=not errors, errors=errors)

    def _validate_type(self, key: str, expected: Any, value: Any, errors: List[str]) -> None:
        if isinstance(expected, dict):
            if not isinstance(value, dict):
                errors.append(f"Expected object for {key}, got {type(value).__name__}")
                return

            nested_required = expected.get("required", {})
            nested_optional = expected.get("optional", {})
            nested_schema = {"required": nested_required, "optional": nested_optional}
            nested_result = self.validate(nested_schema, value)
            errors.extend([f"{key}.{err}" for err in nested_result.errors])
            return

        expected_type = self.VALID_TYPES.get(expected)
        if expected_type is None:
            errors.append(f"Unknown schema type for {key}: {expected}")
            return

        if not isinstance(value, expected_type):
            errors.append(f"Invalid type for {key}: expected {expected}, got {type(value).__name__}")
