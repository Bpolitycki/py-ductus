"""Test the XSL types."""
import pytest
from saxonche import PySaxonProcessor, PyXdmArray, PyXdmAtomicValue

from py_ductus.steps import xsl


def test_if_atomic_is_valid_type():
    """Test that an atomic type is valid."""
    test_type = xsl.XSLAtomicParam(value="test", name="test")
    assert isinstance(test_type, xsl.XSLParam)


@pytest.mark.parametrize(
    "input_value",
    [
        "test",
        "foo",
        1,
        1.0,
        True,
        False,
    ],
)
def test_if_atomic_convert_returns_xdm_atomic(input_value: str | bool | int | float):
    """Test that the atomic convert returns a XdmAtomicValue."""
    test_type = xsl.XSLAtomicParam(value=input_value, name="test")
    proc = PySaxonProcessor()
    assert isinstance(test_type.convert_to_saxon(proc), PyXdmAtomicValue)


def test_if_unsupported_atomic_convert_raises_error():
    """Test that an unsupported atomic type raises an error."""
    test_type = xsl.XSLAtomicParam(value=object(), name="test")  # type: ignore
    proc = PySaxonProcessor()
    with pytest.raises(TypeError):
        test_type.convert_to_saxon(proc)


def test_apply_atomic_parameter():
    """Test that an atomic parameter is applied to the processor."""
    test_type = xsl.XSLAtomicParam(value="test", name="test")
    with PySaxonProcessor(license=False) as proc:
        xsl_proc = proc.new_xslt30_processor()
        test_type.apply_param(proc, xsl_proc)
        assert xsl_proc.get_parameter("test").__str__() == "test"  # type: ignore


def test_if_array_is_valid_type():
    """Test that an array type is valid."""
    test_type = xsl.XSLArrayParam(value=["test"], name="test")
    assert isinstance(test_type, xsl.XSLParam)


@pytest.mark.parametrize(
    "input_value",
    [
        ["test"],
        [1],
        [1.0],
        [True],
        [False],
    ],
)
def test_if_array_convert_returns_xdm_array(input_value: list[str | bool | int | float]):
    """Test that the array convert returns a XdmArray."""
    test_type = xsl.XSLArrayParam(value=input_value, name="test")
    with PySaxonProcessor(license=False) as proc:
        sax_array = test_type.convert_to_saxon(proc)
        assert isinstance(test_type.convert_to_saxon(proc), PyXdmArray)
        assert sax_array.size == 1  # type: ignore
