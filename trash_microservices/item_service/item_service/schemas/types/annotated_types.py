from typing import Any, Annotated

from pydantic import AfterValidator

from item_service.schemas.exceptions.exceptions import FieldValidationException

from loguru import logger

def is_positive(v: int) -> int:
    if v <= 0:
        msg = "Field value must be positive"
        logger.error(msg)
        raise FieldValidationException(msg)
    return v

def is_integer(v: Any) -> int:
    if type(v) is not int:
        msg = "Field value must be an integer"
        logger.error(msg)
        raise FieldValidationException(msg)
    return v

def is_float(v: Any) -> float:
    if type(v) is not float:
        msg = "Field value must be a float"
        logger.error(msg)
        raise FieldValidationException(msg)
    return v


PositiveInteger = Annotated[int, AfterValidator(is_positive), AfterValidator(is_integer)]
PositiveFloat = Annotated[float, AfterValidator(is_positive), AfterValidator(is_float)]
