"""Module for the XSL step."""
from collections.abc import Callable, Iterable
from pathlib import Path

from saxonche import PySaxonProcessor, PyXslt30Processor, PyXsltExecutable

from py_ductus.steps.error import StepError
from py_ductus.steps.xsl.types import XSLParam

AtomicType = str | int | float | bool


class XSL:
    """A XSL step.

    This step applies a XSL transformation to the input values.
    """

    _name: str = "xsl"
    dynamic_params: Callable[[], XSLParam] | list[Callable[..., XSLParam]] | None
    proc_params: XSLParam | list[XSLParam] | None
    xslt: str | Path

    def __init__(
        self,
        xslt: str | Path,
        params: XSLParam | list[XSLParam] | None = None,
        dynamic_params: Callable[[], XSLParam] | list[Callable[[], XSLParam]] | None = None,
    ):
        """Initialize a XSL step.

        Initialize a XSL step with the stylesheet and parameters.

        Args:
            xslt (str | Path): The XSL stylesheet.
            params (XSLParam | list[XSLParam] | None): The parameters for the XSL transformation.
            dynamic_params (Callable[[], XSLParam] | list[Callable[[], XSLParam]] | None): Dynamic parameters for the XSL transformation, which are evaluated for each input value.
        """
        self.xslt = xslt
        self.proc_params = params
        self.dynamic_params = dynamic_params

    def __call__(self, values: Iterable[str]) -> Iterable[str]:
        """Apply the XSL transformation to the input values.

        Args:
            values (list[str]): The input values.

        Returns:
            list[str]: The transformed values.

        Raises:
            StepError: When the XSL transformation fails.
        """
        with PySaxonProcessor(license=False) as proc:
            xsl_proc = proc.new_xslt30_processor()

            self._apply_params(proc=proc, xsl_proc=xsl_proc)

            xslt_executable: PyXsltExecutable = xsl_proc.compile_stylesheet(stylesheet_text=self.xslt) if isinstance(self.xslt, str) else xsl_proc.compile_stylesheet(stylesheet_file=str(self.xslt))  # type: ignore

            result: str | list[str]
            if isinstance(values, str):
                result = self._apply_xslt(input_value=values, proc=proc, xsl_exec=xslt_executable)
            else:
                result = [
                    self._apply_xslt(input_value=value, proc=proc, xsl_exec=xslt_executable)
                    for value in values
                ]

        return result

    def _apply_params(self, proc: PySaxonProcessor, xsl_proc: PyXslt30Processor) -> None:
        if self.proc_params is None:
            return

        if isinstance(self.proc_params, list):
            for param in self.proc_params:
                param.apply_param(proc, xsl_proc)
        else:
            self.proc_params.apply_param(proc, xsl_proc)

    def _apply_dynamic_params(self, proc: PySaxonProcessor, xsl_proc: PyXslt30Processor) -> None:
        if self.dynamic_params is None:
            return

        if isinstance(self.dynamic_params, list):
            for param in self.dynamic_params:
                param().apply_param(proc, xsl_proc)
        else:
            self.dynamic_params().apply_param(proc, xsl_proc)

    def _apply_xslt(
        self, input_value: str, proc: PySaxonProcessor, xsl_exec: PyXsltExecutable
    ) -> str:
        self._apply_dynamic_params(proc=proc, xsl_proc=xsl_exec)

        result: str | None = xsl_exec.transform_to_string(
            xdm_node=proc.parse_xml(xml_text=input_value)
        )

        if result is None:
            raise StepError(step=self, value=input_value)

        return result

    @property
    def name(self) -> str:
        """The name of the step.

        Returns:
            str: The name of the step.
        """
        return self._name
