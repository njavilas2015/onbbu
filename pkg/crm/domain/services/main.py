from dataclasses import dataclass
from pkg.crm.domain.services.discount_service import DiscountService
from pkg.crm.infrastructure.persistence.repositories.main import Repository


@dataclass(frozen=True, slots=True)
class ServiceRegistry:
    discountService: DiscountService


@dataclass(frozen=True, slots=True)
class ServicesContext:
    Repo: Repository


class NewService:

    def __init__(self, ctx: ServicesContext):
        self.ctx = ctx

    def init(self) -> ServiceRegistry:

        discountService = DiscountService(repository=self.ctx.Repo.discountRepo)

        return ServiceRegistry(discountService=discountService)
