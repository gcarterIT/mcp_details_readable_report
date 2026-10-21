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
    if schema.get("type") == "object" and schema.get("properties") == {}:
        return SchemaPresentation(
            status=SchemaPresentationStatus.RECOGNIZED,
            parameters=(),
        )

    return SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )