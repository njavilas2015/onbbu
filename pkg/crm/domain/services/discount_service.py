from onbbu.paginate import Paginate, PaginateDTO

from pkg.crm.application.dtos.create_discount_dto import CreateDiscountDTO
from pkg.crm.application.dtos.delete_discount_dto import DeleteDiscountDTO
from pkg.crm.application.dtos.discount_output_dto import DiscountOutputDTO
from pkg.crm.application.dtos.update_discount_dto import UpdateDiscountDTO

from pkg.crm.application.use_cases.create_discount_usecases import CreateDiscount
from pkg.crm.application.use_cases.delete_discount_usecases import DeleteDiscount
from pkg.crm.application.use_cases.get_all_discounts_usecases import GetAllDiscounts
from pkg.crm.application.use_cases.get_discount_usecases import GetDiscount
from pkg.crm.application.use_cases.update_discount_usecases import UpdateDiscount

from pkg.crm.infrastructure.persistence.repositories.discount_repository import (
    DiscountRepository,
)


class DiscountService:

    def __init__(self, repository: DiscountRepository):
        self.create_discount = CreateDiscount(repository)
        self.get_discount = GetDiscount(repository)
        self.update_discount = UpdateDiscount(repository)
        self.delete_discount = DeleteDiscount(repository)
        self.get_all_discounts = GetAllDiscounts(repository)

    async def create(self, dto: CreateDiscountDTO) -> DiscountOutputDTO:
        return await self.create_discount.execute(dto)

    async def get(self, discount_id: str):
        return await self.get_discount.execute(discount_id)

    async def update(self, dto: UpdateDiscountDTO) -> DiscountOutputDTO:
        return await self.update_discount.execute(dto)

    async def delete(self, dto: DeleteDiscountDTO) -> None:
        return await self.delete_discount.execute(dto)

    async def get_all(self, dto: PaginateDTO) -> Paginate[DiscountOutputDTO]:
        return await self.get_all_discounts.execute(dto)
