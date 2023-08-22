"""Test py-ductus."""

import py_ductus


def test_import_and_name() -> None:
    """Test that the package can be imported and the name is correct."""
    pkg_name = py_ductus.__name__
    assert isinstance(pkg_name, str)
    assert pkg_name == "py_ductus"
