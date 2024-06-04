"""Param types for XSL steps."""

from builtins import bool, float
from typing import Generic, Protocol, TypeVar, runtime_checkable

from saxonche import (
    PySaxonProcessor,
    PyXdmArray,
    PyXdmAtomicValue,
    PyXdmMap,
    PyXdmValue,
    PyXslt30Processor,
    create_xdm_dict,
)

AtomicType = str | int | float | bool

TXdmValue_co = TypeVar("TXdmValue_co", PyXdmAtomicValue, PyXdmArray, PyXdmMap, covariant=True)
TAtomic = TypeVar("TAtomic", AtomicType, list[AtomicType], dict[str, AtomicType | list[AtomicType]])


@runtime_checkable
class XSLParam(Protocol, Generic[TXdmValue_co, TAtomic]):
    """Protocol for XSL Parameters."""

    name: str | None
    value: TAtomic

    def __init__(
        self,
        name: str | None,
        value: TAtomic,
    ) -> None:
        """Initialize a XSLParam.

        Args:
            name (str | None): The name of the parameter.
            value (AtomicType | list[AtomicType] | dict[str, AtomicType | list[AtomicType]]): The value of the parameter.
        """
        ...

    def convert_to_saxon(self, proc: PySaxonProcessor) -> TXdmValue_co:
        """Convert the parameter to a Saxon parameter.

        Raises:
            TypeError: When the type of the parameter is not supported.

        Returns:
            PyXdmAtomicValue | PyXdmArray | PyXdmMap: The Saxon parameter.
        """
        ...

    def apply_param(self, proc: PySaxonProcessor, xsl_proc: PyXslt30Processor) -> None:
        """Apply the parameter to the processor.

        Args:
            proc (PySaxonProcessor): The processor to apply the parameter to.
            xsl_proc (PyXslt30Processor): The processor to apply the parameter to.
        """
        ...


class XSLAtomicParam:
    """A (saxon) XSL Atomic Parameter."""

    name: str | None
    value: AtomicType | PyXdmValue

    def __init__(self, name: str | None, value: AtomicType) -> None:
        """Initialize a XSLAtomicParam.

        Args:
            name (str): The name of the parameter.
            value (AtomicType): The value of the parameter.
        """
        self.name = name
        self.value = value

    def convert_to_saxon(self, proc: PySaxonProcessor) -> PyXdmAtomicValue | PyXdmValue:
        """Convert the parameter to a Saxon parameter.

        Raises:
            TypeError: When the type of the parameter is not supported.

        Returns:
            PyXdmAtomicValue: The Saxon parameter.
        """
        if isinstance(self.value, str):
            return proc.make_string_value(self.value)
        if isinstance(self.value, int):
            return proc.make_integer_value(self.value)
        if isinstance(self.value, bool):
            return proc.make_boolean_value(self.value)
        if isinstance(self.value, float):
            return proc.make_float_value(self.value)  # type: ignore
        if isinstance(self.value, PyXdmValue):
            return self.value
        raise TypeError(f"Unsupported type {type(self.value)}")

    def apply_param(self, proc: PySaxonProcessor, xsl_proc: PyXslt30Processor) -> None:
        """Apply the parameter to the processor.

        Args:
            proc (PySaxonProcessor): The processor to apply the parameter to.
            xsl_proc (PyXslt30Processor): The processor to apply the parameter to.
        """
        if self.name is not None:
            xsl_proc.set_parameter(self.name, self.convert_to_saxon(proc))


class XSLArrayParam:
    """A (saxon) XSL Array Parameter."""

    name: str | None
    value: list[AtomicType]

    def __init__(self, name: str | None, value: list[AtomicType]) -> None:
        """Initialize a XSLArray.

        Args:
            name (str): The name of the parameter.
            value (list[XSLAtomicParam]): The value of the parameter.
        """
        self.name = name
        self.value = value

    def convert_to_saxon(self, proc: PySaxonProcessor) -> PyXdmArray:
        """Convert the parameter to a Saxon parameter.

        Raises:
            TypeError: When the type of the parameter is not supported.

        Returns:
            PyXdmArray: The Saxon parameter.
        """
        return proc.make_array(  # type: ignore
            [XSLAtomicParam(value=val, name=None).convert_to_saxon(proc=proc) for val in self.value]
        )

    def apply_param(self, proc: PySaxonProcessor, xsl_proc: PyXslt30Processor) -> None:
        """Apply the parameter to the processor.

        Args:
            proc (PySaxonProcessor): The processor to apply the parameter to.
            xsl_proc (PyXslt30Processor): The processor to apply the parameter to.
        """
        if self.name is not None:
            xsl_proc.set_parameter(self.name, self.convert_to_saxon(proc))


# Note this is not used yet, because create_xdm_dict seems to be buggy
class XSLMapParam:
    """A (saxon) XSL Map Parameter."""

    name: str
    value: dict[str, AtomicType | list[AtomicType]]

    def __init__(self, name: str, value: dict[str, AtomicType | list[AtomicType]]) -> None:
        """Initialize a XSLMapParam.

        Args:
            name (str): The name of the parameter.
            value (dict[str, AtomicType | list[AtomicType]]): The value of the parameter.
        """
        self.name = name
        self.value = value

    def convert_to_saxon(self, proc: PySaxonProcessor) -> PyXdmMap:
        """Convert the parameter to a Saxon parameter.

        Raises:
            TypeError: When the type of the parameter is not supported.

        Returns:
            PyXdmMap: The Saxon parameter.
        """
        xdm_data_dict = create_xdm_dict(
            proc,
            {
                key: (
                    XSLArrayParam(value=value, name=None).convert_to_saxon(proc=proc)
                    if isinstance(value, list)
                    else XSLAtomicParam(value=value, name=None).convert_to_saxon(proc=proc)
                )
                for key, value in self.value.items()
            },
        )

        return proc.make_map(xdm_data_dict)  # type: ignore

    def apply_param(self, proc: PySaxonProcessor, xsl_proc: PyXslt30Processor) -> None:
        """Apply the parameter to the processor.

        Args:
            proc (PySaxonProcessor): The processor to apply the parameter to.
            xsl_proc (PyXslt30Processor): The processor to apply the parameter to.
        """
        xsl_proc.set_parameter(self.name, self.convert_to_saxon(proc))
