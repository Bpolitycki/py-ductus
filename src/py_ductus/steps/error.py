"""Error classes for steps."""

from typing import Generic

from py_ductus.common import types
from py_ductus.steps.protocol import Step


class StepError(Exception, Generic[types.TContent]):
    """Error raised when a step fails processing."""

    def __init__(self, step: Step, value: types.TContent) -> None:
        """Initialize a StepError.

        Args:
            message (str): The error message.
            step (Step): The step that raised the error.
            value (T): The value that caused the error.
        """
        super().__init__(f"Error while applying step '{step.name}' to input value {value}.")
