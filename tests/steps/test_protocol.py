"""Test the step protocol using fake steps."""

from py_ductus.steps.protocol import Step
from tests.conftest import InvalidFakeStep, ValidFakeStep


def test_if_valid_step_is_valid() -> None:
    """Test that a valid step is ok."""
    step = ValidFakeStep()
    assert isinstance(step, Step)
    assert isinstance(step.name, str)
    assert step.name == "valid_fake_step"


def test_if_invalid_step_is_invalid() -> None:
    """Test that an invalid step is invalid."""
    step = InvalidFakeStep()
    assert not isinstance(step, Step)  # type: ignore
    assert not hasattr(step, "name")
