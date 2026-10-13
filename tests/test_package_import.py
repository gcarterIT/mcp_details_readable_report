"""Tests for the package import boundary."""


def test_package_imports() -> None:
    """The readable-report package should be importable."""
    import mcp_details_readable_report

    assert mcp_details_readable_report is not None