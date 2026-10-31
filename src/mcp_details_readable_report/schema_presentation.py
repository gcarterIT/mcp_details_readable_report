"""Presentation models for readable schema interpretation."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class SchemaPresentationStatus(Enum):
    """Status of readable schema interpretation."""

    RECOGNIZED = "recognized"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class DefaultPresentation:
    """Presentation evidence for an explicitly supplied schema default."""

    value: object


@dataclass(frozen=True)
class ParameterPresentation:
    """Readable presentation facts for one schema parameter."""

    name: str
    type_name: str | None
    required: bool
    description: str | None
    allowed_values: tuple[object, ...] | None = None
    default: DefaultPresentation | None = None


@dataclass(frozen=True)
class SchemaPresentation:
    """Readable presentation of an interpreted schema."""

    status: SchemaPresentationStatus
    parameters: tuple[ParameterPresentation, ...]


def _is_primitive_presentation_value(value: object) -> bool:
    """Return whether a value fits the current primitive presentation boundary."""
    return value is None or isinstance(value, (str, int, float, bool))


def _is_supported_primitive_any_of(property_schema: dict[str, Any]) -> bool:
    """Return whether present anyOf evidence fits the primitive presentation boundary."""
    any_of = property_schema.get("anyOf")

    return (
        isinstance(any_of, list)
        and all(
            isinstance(alternative, dict)
            and isinstance(alternative.get("type"), str)
            for alternative in any_of
        )
    )


def _interpret_type_name(property_schema: dict[str, Any]) -> str | None:
    """Derive a readable type name from supported property schema evidence."""
    direct_type = property_schema.get("type")

    if isinstance(direct_type, str):
        return direct_type

    if _is_supported_primitive_any_of(property_schema):
        return " | ".join(
            alternative["type"]
            for alternative in property_schema["anyOf"]
        )

    return None





def interpret_schema(schema: dict[str, Any]) -> SchemaPresentation:
    """Interpret supported schema evidence for readable presentation."""
    properties = schema.get("properties")

    if schema.get("type") == "object" and properties == {}:
        return SchemaPresentation(
            status=SchemaPresentationStatus.RECOGNIZED,
            parameters=(),
        )

    if schema.get("type") == "object" and isinstance(properties, dict):
        if not all(isinstance(property_schema, dict) for property_schema in properties.values()):
            return SchemaPresentation(
                status=SchemaPresentationStatus.UNSUPPORTED,
                parameters=(),
            )

        required = schema.get("required", [])

        if not isinstance(required, list):
            return SchemaPresentation(
                status=SchemaPresentationStatus.UNSUPPORTED,
                parameters=(),
            )

        if any(
            "enum" in property_schema
            and (
                not isinstance(property_schema["enum"], list)
                or not all(
                    _is_primitive_presentation_value(value)
                    for value in property_schema["enum"]
                )
            )
            for property_schema in properties.values()
        ):
            return SchemaPresentation(
                status=SchemaPresentationStatus.UNSUPPORTED,
                parameters=(),
            )

        if any(
            "anyOf" in property_schema
            and not _is_supported_primitive_any_of(property_schema)
            for property_schema in properties.values()
        ):
            return SchemaPresentation(
                status=SchemaPresentationStatus.UNSUPPORTED,
                parameters=(),
            )

        if any(
            "default" in property_schema
            and not _is_primitive_presentation_value(property_schema["default"])
            for property_schema in properties.values()
        ):
            return SchemaPresentation(
                status=SchemaPresentationStatus.UNSUPPORTED,
                parameters=(),
            )

        parameters = tuple(
            ParameterPresentation(
                name=name,
                type_name=_interpret_type_name(property_schema),
                required=name in required,
                description=property_schema.get("description"),
                allowed_values=(
                    tuple(property_schema["enum"])
                    if isinstance(property_schema.get("enum"), list)
                    else None
                ),
                default=(
                    DefaultPresentation(value=property_schema["default"])
                    if "default" in property_schema
                    else None
                ),
            )
            for name, property_schema in properties.items()
        )

        return SchemaPresentation(
            status=SchemaPresentationStatus.RECOGNIZED,
            parameters=parameters,
        )

    return SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )
