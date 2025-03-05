from pkg.crm.application.dtos.create_discount_dto import CreateDiscountDTO
from pkg.crm.application.dtos.discount_output_dto import DiscountOutputDTO

from pkg.crm.domain.entities.discount_entity import DiscountEntity
from pkg.crm.infrastructure.logger.discount_logger import DiscountLogger
from pkg.crm.infrastructure.persistence.repositories.discount_repository import DiscountRepository
from pkg.crm.infrastructure.transformers.discount_transformer import DiscountTransformer


class CreateDiscount:
    transformer: DiscountTransformer
    repository: DiscountRepository

    def __init__(self, repository: DiscountRepository):
        self.transformer = DiscountTransformer()
        self.repository = repository

    async def execute(self, dto: CreateDiscountDTO) -> DiscountOutputDTO:

        if self.repository.get_by_name(dto):
            raise ValueError("There is already a discount with this name.")

        discount: DiscountEntity = await self.repository.create(dto)

        DiscountLogger.log_creation(discount)

        return self.transformer.transform_discount_to_output(discount)
