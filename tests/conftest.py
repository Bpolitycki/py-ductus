"""Common fixtures and fakes for testing."""

from collections.abc import Iterable
from pathlib import Path
from typing import Generic

import pytest

from py_ductus.common import types


class ValidFakeStep(Generic[types.TContent]):
    """A valid fake step."""

    def __init__(self) -> None:
        """Initialize the step."""
        self._name = "valid_fake_step"

    def __call__(self, values: Iterable[types.TContent]) -> Iterable[types.TContent]:
        """Process values with the step."""
        return values

    @property
    def name(self) -> str:
        """The name of the step."""
        return self._name


class InvalidFakeStep(Generic[types.TContent]):
    """An invalid fake step."""

    def __init__(self) -> None:
        """Initialize the step."""

    def __call__(self, values: types.TContent) -> types.TContent:
        """Process values with the step."""
        return "foo"  # type: ignore


@pytest.fixture()
def xml_xsl_sample(tmp_path: Path) -> tuple[str, str, Path]:
    """Return a sample XML and XSL file."""
    xsl = """
    <!-- identity.xsl -->
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Identity template -->
  <xsl:template match="@* | node()">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
    """
    xml = """<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>"""
    with open(tmp_path / "identity.xsl", "w") as f:
        f.write(xsl)

    return xml, xsl, tmp_path / "identity.xsl"
