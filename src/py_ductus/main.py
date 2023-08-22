from collections.abc import Iterable  # noqa: D100
from functools import reduce

from py_ductus.common.types import T
from py_ductus.steps.protocol import Step


def process(input_values: Iterable[T], steps: tuple[Step]) -> Iterable[T]:
    """Process values with steps.

    Args:
        input_values (Iterable[T]): The values to process.
        steps (Iterable[Step]): The steps to process the values with.

    Returns:
        Iterable[T]: The processed values.
    """
    return reduce(lambda values, step: step(values), steps, input_values)
