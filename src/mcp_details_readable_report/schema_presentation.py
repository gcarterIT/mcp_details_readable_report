"""Presentation models for readable schema interpretation."""

from dataclasses import dataclass
from enum import Enum


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