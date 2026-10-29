"""Tests for schema presentation models."""

from mcp_details_readable_report.schema_presentation import (
    DefaultPresentation,
    ParameterPresentation,
    SchemaPresentation,
    SchemaPresentationStatus,
    interpret_schema,
)


def test_parameter_presentation_preserves_simple_parameter_facts() -> None:
    """A parameter presentation should preserve its derived display facts."""
    parameter = ParameterPresentation(
        name="width",
        type_name="number",
        required=True,
        description="Width of the browser window",
    )

    assert parameter.name == "width"
    assert parameter.type_name == "number"
    assert parameter.required is True
    assert parameter.description == "Width of the browser window"


def test_schema_presentation_can_represent_recognized_zero_parameters() -> None:
    """A recognized schema may legitimately contain no parameters."""
    presentation = SchemaPresentation(
        status=SchemaPresentationStatus.RECOGNIZED,
        parameters=(),
    )

    assert presentation.status is SchemaPresentationStatus.RECOGNIZED
    assert presentation.parameters == ()


def test_schema_presentation_distinguishes_unsupported_schema() -> None:
    """Unsupported interpretation must differ from recognized zero parameters."""
    presentation = SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )

    assert presentation.status is SchemaPresentationStatus.UNSUPPORTED
    assert presentation.parameters == ()

    
def test_interpret_schema_recognizes_empty_object_parameters() -> None:
    """An object with empty properties is a recognized zero-parameter schema."""
    schema = {
        "type": "object",
        "properties": {},
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.RECOGNIZED,
        parameters=(),
    )
    
def test_interpret_schema_marks_unhandled_root_type_as_unsupported() -> None:
    """An unhandled root schema type must not masquerade as zero parameters."""
    schema = {
        "type": "array",
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )
    
def test_interpret_schema_presents_single_required_number_parameter() -> None:
    """A simple required number property should become a readable parameter."""
    schema = {
        "type": "object",
        "properties": {
            "width": {
                "type": "number",
                "description": "Width of the browser window",
            },
        },
        "required": ["width"],
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.RECOGNIZED,
        parameters=(
            ParameterPresentation(
                name="width",
                type_name="number",
                required=True,
                description="Width of the browser window",
            ),
        ),
    )

def test_interpret_schema_does_not_mutate_input_schema() -> None:
    """Schema interpretation must not mutate authoritative input evidence."""
    schema = {
        "type": "object",
        "properties": {},
    }
    original_schema = {
        "type": "object",
        "properties": {},
    }

    interpret_schema(schema)

    assert schema == original_schema

def test_interpret_schema_presents_multiple_simple_parameters_in_source_order() -> None:
    """Multiple simple properties should preserve source order and requiredness."""
    schema = {
        "type": "object",
        "properties": {
            "width": {
                "type": "number",
                "description": "Width of the browser window",
            },
            "timeout": {
                "type": "number",
                "description": "Maximum time to wait",
            },
        },
        "required": ["width"],
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.RECOGNIZED,
        parameters=(
            ParameterPresentation(
                name="width",
                type_name="number",
                required=True,
                description="Width of the browser window",
            ),
            ParameterPresentation(
                name="timeout",
                type_name="number",
                required=False,
                description="Maximum time to wait",
            ),
        ),
    )


def test_interpret_schema_presents_single_optional_parameter() -> None:
    """A property absent from required should be presented as optional."""
    schema = {
        "type": "object",
        "properties": {
            "timeout": {
                "type": "number",
                "description": "Maximum time to wait",
            },
        },
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.RECOGNIZED,
        parameters=(
            ParameterPresentation(
                name="timeout",
                type_name="number",
                required=False,
                description="Maximum time to wait",
            ),
        ),
    )


def test_interpret_schema_marks_non_mapping_property_schema_as_unsupported() -> None:
    """An unfamiliar property shape should fall back instead of raising."""
    schema = {
        "type": "object",
        "properties": {
            "width": "unexpected",
        },
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )


def test_interpret_schema_marks_none_required_as_unsupported() -> None:
    """An unfamiliar required shape should fall back instead of raising."""
    schema = {
        "type": "object",
        "properties": {
            "width": {
                "type": "number",
            },
        },
        "required": None,
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )


def test_interpret_schema_marks_string_required_as_unsupported() -> None:
    """A string required value should not be interpreted as a name collection."""
    schema = {
        "type": "object",
        "properties": {
            "width": {
                "type": "number",
            },
        },
        "required": "width",
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )


def test_default_presentation_can_preserve_explicit_null() -> None:
    """An explicit null default should remain representable."""
    default = DefaultPresentation(value=None)

    assert default.value is None


def test_parameter_presentation_can_represent_absent_default() -> None:
    """A parameter should distinguish an absent default."""
    parameter = ParameterPresentation(
        name="level",
        type_name="string",
        required=False,
        description="Minimum message level",
        allowed_values=None,
        default=None,
    )

    assert parameter.default is None


def test_parameter_presentation_can_preserve_enum_and_default() -> None:
    """Primitive enum choices and a default should be representable."""
    parameter = ParameterPresentation(
        name="level",
        type_name="string",
        required=False,
        description="Minimum message level",
        allowed_values=("error", "warning", "info"),
        default=DefaultPresentation(value="info"),
    )

    assert parameter.allowed_values == ("error", "warning", "info")
    assert parameter.default == DefaultPresentation(value="info")


def test_interpret_schema_presents_primitive_string_enum_values() -> None:
    """Primitive string enum values should become immutable allowed values."""
    schema = {
        "type": "object",
        "properties": {
            "level": {
                "type": "string",
                "description": "Minimum message level",
                "enum": ["error", "warning", "info", "debug"],
            },
        },
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.RECOGNIZED,
        parameters=(
            ParameterPresentation(
                name="level",
                type_name="string",
                required=False,
                description="Minimum message level",
                allowed_values=("error", "warning", "info", "debug"),
                default=None,
            ),
        ),
    )


def test_interpret_schema_marks_string_enum_as_unsupported() -> None:
    """A string enum should not be treated as absent enum evidence."""
    schema = {
        "type": "object",
        "properties": {
            "level": {
                "type": "string",
                "enum": "error",
            },
        },
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )


def test_interpret_schema_marks_complex_enum_values_as_unsupported() -> None:
    """Complex enum members should use graceful unsupported fallback."""
    schema = {
        "type": "object",
        "properties": {
            "mode": {
                "type": "object",
                "enum": [
                    {"name": "fast"},
                    {"name": "safe"},
                ],
            },
        },
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
    )
