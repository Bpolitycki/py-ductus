from abc import abstractmethod  # noqa: D100
from collections.abc import Iterable
from typing import Generic, Protocol, runtime_checkable

from py_ductus.common import types


@runtime_checkable
class Step(Protocol, Generic[types.TContent]):
    """Protocol for Steps in a pipeline.

    Steps are a single unit in a processing pipeline,
    which is composed multiple steps.
    """

    _name: str

    @abstractmethod
    def __call__(self, values: Iterable[types.TContent]) -> Iterable[types.TContent]:
        """The call method of the step.

        A step is a callable that takes iterable of (generic) values of type T
        and returns the processed values as an iterable.

        Args:
            values (Iterable[TContent]): The values to process.

        Returns:
            Iterable[TContent]: The processed values.

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
