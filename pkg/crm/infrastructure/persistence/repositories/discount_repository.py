from typing import Optional
from dataclasses import asdict

from onbbu.paginate import PaginateDTO

from pkg.crm.domain.entities.discount_entity import DiscountEntity
from pkg.crm.application.dtos.create_discount_dto import CreateDiscountDTO
from pkg.crm.application.dtos.update_discount_dto import UpdateDiscountDTO

from pkg.crm.infrastructure.persistence.models.discount_model import (
    DiscountModel,
)


class DiscountRepository:
    async def get_all(self, dto: PaginateDTO) -> tuple[list[DiscountEntity], int]:

        total: int = await DiscountModel.all().count()
        
        print(total)

        queryset: list[DiscountEntity] = [
            DiscountEntity(**instance.to_dict())
            for instance in await DiscountModel.filter(id__gt=dto.page * dto.limit)
            .order_by("id")
            .limit(dto.limit)
            .all()
        ]


        return queryset, total

    async def get_total_count(self) -> int:
        return await DiscountModel.all().count()

    async def exist_by_id(self, id: int) -> bool:
        return await DiscountModel.filter(id=id).exists()

    async def exist_by_name(self, name: str) -> bool:
        return await DiscountModel.filter(name=name).exists()

    async def get_by_id(self, id: int) -> Optional[DiscountEntity]:

        if not await self.exist_by_id(id):
            return None

        instance: DiscountModel = await DiscountModel.get(id=id)

        return DiscountEntity(**instance.to_dict())

    async def get_by_name(self, name: str) -> Optional[DiscountEntity]:

        if not await self.exist_by_name(name):
            return None

        instance: DiscountModel = await DiscountModel.get(name=name)

        return DiscountEntity(**instance.to_dict())

    async def create(self, dto: CreateDiscountDTO) -> DiscountEntity:

        instance: DiscountModel = await DiscountModel.create(**asdict(dto))

        return DiscountEntity(**instance.to_dict())

    async def update_by_id(self, dto: UpdateDiscountDTO) -> Optional[DiscountEntity]:

        if not await self.exist_by_id(id):
            return None

        instance: DiscountModel = await DiscountModel.get(id=dto.id)

        for field, value in asdict(dto).items():
            setattr(instance, field, value)

        await instance.save()

        return DiscountEntity(**instance.to_dict())

    async def delete_by_id(self, id: int) -> Optional[DiscountEntity]:

        if not await self.exist_by_id(id):
            return None

        instance: DiscountModel = await DiscountModel.get(id=id)

        await instance.delete()

        return instance
