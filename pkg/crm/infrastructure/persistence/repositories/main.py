from dataclasses import dataclass

from pkg.crm.infrastructure.persistence.repositories.discount_repository import (
    DiscountRepository,
)


@dataclass(frozen=True, slots=True)
class Repository:
    discountRepo: DiscountRepository


class NewRepository:

    def __init__(self):
        self.repos = Repository(discountRepo=DiscountRepository())

    def init(self) -> Repository:
        return self.repos

    def migrate(self):
        pass

    def drop(self):
        pass
