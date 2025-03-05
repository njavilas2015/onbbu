from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiscountEntity:
    id: int
    name: str
    percentage: float
    is_visible: bool