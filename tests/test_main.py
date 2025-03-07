"""Test the main.py file."""

from pathlib import Path

from py_ductus.main import process
from py_ductus.steps import xsl
from py_ductus.steps.protocol import StepAlternative
from tests.conftest import FailingFakeStep, ValidFakeStep


def test_process_with_xsl_step(xml_xsl_sample: tuple[str, str, Path]):
    """Test that the process function works with an XSL step."""
    xml, xslt, _ = xml_xsl_sample
    step = xsl.XSL(xslt=xslt)
    assert process([xml], steps=[step]) == [xml]


def test_process_with_xsl_and_fake(xml_xsl_sample: tuple[str, str, Path]):
    """Test that the process function works with an XSL step."""
    xml, xslt, _ = xml_xsl_sample
    step = xsl.XSL(xslt=xslt)
    fake = ValidFakeStep()
    assert process([xml, xml, xml], steps=[step, fake]) == [xml, xml, xml]


def test_process_with_xsl_and_fake_alternative(xml_xsl_sample: tuple[str, str, Path]):
    """Test that the process function works with an XSL step."""
    xml, xslt, _ = xml_xsl_sample
    step = xsl.XSL(xslt=xslt)
    fake = ValidFakeStep()
    failing = FailingFakeStep()
    assert process([xml, xml, xml], steps=[step, StepAlternative(main=failing, fallback=fake)]) == [  # type: ignore
        xml,
        xml,
        xml,
    ]
