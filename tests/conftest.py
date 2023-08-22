"""Common fixtures and fakes for testing."""

from collections.abc import Iterable

from py_ductus.common import types


class ValidFakeStep:
    """A valid fake step."""

    def __init__(self) -> None:
        """Initialize the step."""
        self._name = "valid_fake_step"

    def __call__(self, values: Iterable[types.T]) -> Iterable[types.T]:
        """Process values with the step."""
        return values

    @property
    def name(self) -> str:
        """The name of the step."""
        return self._name


class InvalidFakeStep:
    """An invalid fake step."""

    def __init__(self) -> None:
        """Initialize the step."""

    def __call__(self, values: types.T) -> types.T:
        """Process values with the step."""
        return "foo"  # type: ignore
