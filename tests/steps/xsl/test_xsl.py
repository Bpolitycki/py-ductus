"""Test the XSL step."""
from pathlib import Path

from py_ductus.steps import xsl
from py_ductus.steps.protocol import Step


def test_if_xsl_is_a_valid_step():
    """Test that the XSL step is a valid step."""
    assert isinstance(xsl.XSL(xslt=""), Step)
    assert xsl.XSL("").name == "xsl"


def test_xsl_step_applied(xml_xsl_sample: tuple[str, str, Path]):
    """Test that the XSL step is applied."""
    xml, xslt, xsl_path = xml_xsl_sample

    # Test with xslt as a Path
    step = xsl.XSL(xslt=xsl_path)
    assert step(xml) == xml

    # Test with xslt as a str
    step = xsl.XSL(xslt=xslt)
    assert step(xml) == xml
