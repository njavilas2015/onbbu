from pydantic.dataclasses import dataclass
from pydantic import Field


@dataclass(frozen=True, slots=True)
class DeleteDiscountDTO:
    id: int = Field(..., gt=0)
