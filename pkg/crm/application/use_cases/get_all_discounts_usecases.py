from typing import List
from onbbu.paginate import Paginate, PaginateDTO
from pkg.crm.application.dtos.discount_output_dto import DiscountOutputDTO
from pkg.crm.infrastructure.transformers.discount_transformer import DiscountTransformer

from pkg.crm.infrastructure.persistence.repositories.discount_repository import (
    DiscountRepository,
)


class GetAllDiscounts:
    transformer: DiscountTransformer
    repository: DiscountRepository

    def __init__(self, repository: DiscountRepository):
        self.transformer = DiscountTransformer()
        self.repository = repository

    async def execute(self, dto: PaginateDTO) -> Paginate[DiscountOutputDTO]:

        discounts, total = await self.repository.get_all(dto)

        data: List[DiscountOutputDTO] = self.transformer.transform_discounts_to_outputs(
            discounts
        )

        paginate: Paginate[List[DiscountOutputDTO]] = Paginate(
            page=dto.page, limit=dto.limit, total=total, data=data, total_page=0
        )

        return paginate
