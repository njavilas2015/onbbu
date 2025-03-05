from decimal import Decimal

from pydantic.dataclasses import dataclass
from pydantic import Field


@dataclass(frozen=True, slots=True)
class DiscountOutputDTO:
    id: int = Field(alias="id", gt=0)
    name: str = Field(alias="name", min_length=3)
    percentage: Decimal = Field(alias="percentage", ge=0, le=100)
    is_visible: bool = Field(alias="is_visible", default=True)
