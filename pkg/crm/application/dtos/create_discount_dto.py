from decimal import Decimal

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateDiscountDTO:
    name: str = Field(alias="name", min_length=3)
    percentage: Decimal = Field(alias="percentage", ge=0, le=100)
    is_visible: bool = Field(alias="is_visible", default=True)
