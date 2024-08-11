from typing import Any, Annotated

from pydantic import AfterValidator

from src.schemas.exceptions import FieldValidationException

from loguru import logger

def is_positive(v: int) -> int:
    if v <= 0:
        msg = f"Field value must be positive. Given: {v}"
        logger.error(msg)
        raise FieldValidationException(msg)
    return v

def is_integer(v: Any) -> int:
    if type(v) is not int:
        msg = f"Field value must be an integer. Given: {v}"
        logger.error(msg)
        raise FieldValidationException(msg)
    return v

def is_float(v: Any) -> float:
    if type(v) is not float:
        msg = f"Field value must be a float. Given: {v}"
        logger.error(msg)
        raise FieldValidationException(msg)
    return v


PositiveInteger = Annotated[int, AfterValidator(is_positive), AfterValidator(is_integer)]
PositiveFloat = Annotated[float, AfterValidator(is_positive), AfterValidator(is_float)]
