"""Test the XSL step."""

import xml.etree.ElementTree as ET  # noqa: N817
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


def test_xsl_step_applied_with_static_param(xml_xsl_sample_with_params: tuple[str, str, Path]):
    """Test that a XSL step with params is applied correctly."""
    xml, _, xsl_path = xml_xsl_sample_with_params
    xsl_param = xsl.XSLAtomicParam(name="param1", value="bar")

    # Test with a static param
    step = xsl.XSL(xslt=xsl_path, params=xsl_param)
    step_result = step(xml)

    assert isinstance(step_result, str)
    tree = ET.fromstring(step_result)
    text = tree.text
    assert text == "bar"


def test_xsl_step_applied_with_dynamic_param(xml_xsl_sample_with_params: tuple[str, str, Path]):
    """Test that a XSL step with params is applied correctly."""
    xml, _, xsl_path = xml_xsl_sample_with_params

    def xsl_param():
        return xsl.XSLAtomicParam(name="param1", value="foo")

    # Test with a dynamic param
    step = xsl.XSL(xslt=xsl_path, dynamic_params=xsl_param)
    step_result = step([xml, xml])

    assert isinstance(step_result, list)
    assert len(step_result) == 2

    step_result_1 = step_result[0]
    assert isinstance(step_result_1, str)
    tree_1 = ET.fromstring(step_result_1)
    text_1 = tree_1.text

    step_result_2 = step_result[1]
    assert isinstance(step_result_2, str)
    tree_2 = ET.fromstring(step_result_2)
    text_2 = tree_2.text

    assert text_1 == text_2
