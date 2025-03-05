from typing import Optional

from pkg.crm.domain.entities.discount_entity import DiscountEntity

from pkg.crm.application.dtos.update_discount_dto import UpdateDiscountDTO
from pkg.crm.application.dtos.discount_output_dto import DiscountOutputDTO

from pkg.crm.infrastructure.logger.discount_logger import DiscountLogger
from pkg.crm.infrastructure.transformers.discount_transformer import DiscountTransformer

from pkg.crm.infrastructure.persistence.repositories.discount_repository import (
    DiscountRepository,
)


class UpdateDiscount:
    transformer: DiscountTransformer
    repository: DiscountRepository

    def __init__(self, repository: DiscountRepository):
        self.transformer = DiscountTransformer()
        self.repository = repository

    async def execute(self, dto: UpdateDiscountDTO) -> DiscountOutputDTO:

        discount: Optional[DiscountEntity] = await self.repository.update_by_id(dto)

        if not discount:
            raise ValueError("The discount does not exist.")

        DiscountLogger.log_update(discount)

        return self.transformer.transform_discount_to_output(discount)
