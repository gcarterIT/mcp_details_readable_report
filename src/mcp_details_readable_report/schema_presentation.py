"""Presentation models for readable schema interpretation."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class SchemaPresentationStatus(Enum):
    """Status of readable schema interpretation."""

    RECOGNIZED = "recognized"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class ParameterPresentation:
    """Readable presentation facts for a schema parameter."""

    name: str
    type_name: str | None
    required: bool
    description: str | None


@dataclass(frozen=True)
class SchemaPresentation:
    """Readable presentation of an interpreted schema."""

    status: SchemaPresentationStatus
    parameters: tuple[ParameterPresentation, ...]


def interpret_schema(schema: dict[str, Any]) -> SchemaPresentation:
    """Interpret supported schema evidence for readable presentation."""
    properties = schema.get("properties")

    if schema.get("type") == "object" and properties == {}:
        return SchemaPresentation(
            status=SchemaPresentationStatus.RECOGNIZED,
            parameters=(),
        )

    if (
        schema.get("type") == "object"
        and isinstance(properties, dict)
        and len(properties) == 1
    ):
        name, property_schema = next(iter(properties.items()))
        required = schema.get("required", [])

        return SchemaPresentation(
            status=SchemaPresentationStatus.RECOGNIZED,
            parameters=(
                ParameterPresentation(
                    name=name,
                    type_name=property_schema.get("type"),
                    required=name in required,
                    description=property_schema.get("description"),
                ),
            ),
        )

    return SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )