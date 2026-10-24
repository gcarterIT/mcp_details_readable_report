"""Tests for schema presentation models."""

from mcp_details_readable_report.schema_presentation import (
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

def test_interpret_schema_leaves_multiple_properties_unsupported_for_now() -> None:
    """Multiple properties remain unsupported until their behavior is defined."""
    schema = {
        "type": "object",
        "properties": {
            "width": {
                "type": "number",
            },
            "height": {
                "type": "number",
            },
        },
        "required": ["width", "height"],
    }

    presentation = interpret_schema(schema)

    assert presentation == SchemaPresentation(
        status=SchemaPresentationStatus.UNSUPPORTED,
        parameters=(),
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