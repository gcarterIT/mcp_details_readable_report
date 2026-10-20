"""Tests for schema presentation models."""

from mcp_details_readable_report.schema_presentation import (
    ParameterPresentation,
    SchemaPresentation,
    SchemaPresentationStatus,
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
