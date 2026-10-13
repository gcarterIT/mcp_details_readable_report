"""Tests for the MCP Details upstream integration contract."""


def test_application_inspection_result_is_importable() -> None:
    """The selected MCP Details structured-result boundary should be importable."""
    from mcp_details.results import ApplicationInspectionResult

    assert ApplicationInspectionResult is not None