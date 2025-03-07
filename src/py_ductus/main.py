from collections.abc import Iterable  # noqa: D100

from py_ductus.common.types import TContent
from py_ductus.steps.protocol import Step, StepAlternative


def process(
    input_values: Iterable[TContent], steps: Iterable[Step | StepAlternative]
) -> Iterable[TContent]:
    """Process values with steps.

    Args:
        input_values (Iterable[TContent]): The values to process.
        steps (Iterable[Step]): The steps to process the values with.

    Returns:
        Iterable[TContent]: The processed values.
    """
    value_result = input_values

    for step in steps:
        if isinstance(step, StepAlternative):
            try:
                value_result = step.main(value_result)
            except Exception:
                value_result = step.fallback(value_result)
            continue

        value_result = step(value_result)

    return value_result
