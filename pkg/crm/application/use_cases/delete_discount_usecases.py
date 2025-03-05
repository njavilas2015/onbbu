from pkg.crm.application.dtos.delete_discount_dto import DeleteDiscountDTO
from pkg.crm.domain.entities.discount_entity import DiscountEntity
from pkg.crm.infrastructure.transformers.discount_transformer import DiscountTransformer
from pkg.crm.infrastructure.logger.discount_logger import DiscountLogger
from pkg.crm.infrastructure.persistence.repositories.discount_repository import (
    DiscountRepository,
)


class DeleteDiscount:
    transformer: DiscountTransformer
    repository: DiscountRepository

    def __init__(self, repository: DiscountRepository):
        self.transformer = DiscountTransformer()
        self.repository = repository


    async def execute(self, dto: DeleteDiscountDTO) -> None:

        discount: DiscountEntity = await self.repository.delete_by_id(id=dto.id)

        if not discount:
            raise ValueError("The discount does not exist.")

        DiscountLogger.log_deletion(discount)
