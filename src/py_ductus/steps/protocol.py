from abc import abstractmethod  # noqa: D100
from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from py_ductus.common import types


@runtime_checkable
class Step(Protocol):
    """Protocol for Steps in a pipeline.

    Steps are a single unit in a processing pipeline,
    which is composed multiple steps.
    """

    _name: str

    @abstractmethod
    def __call__(self, values: Iterable[types.T]) -> Iterable[types.T]:
        """The call method of the step.

        A step is a callable that takes iterable of (generic) values of type T
        and returns the processed values as an iterable.

        Args:
            values (Iterable[T]): The values to process.

        Returns:
            Iterable[T]: The processed values.

        Raises:
            StepError: When the step fails processing.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the step.

        Returns:
            str: The name of the step.
        """
        ...
