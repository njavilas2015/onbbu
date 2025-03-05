from dataclasses import dataclass
from pydantic import ValidationError

from onbbu.paginate import PaginateDTO
from onbbu import (
    Response,
    ResponseNotFoundError,
    ResponseValidationError,
    ResponseValueError,
    JSONResponse,
    Request
)

from pkg.crm.application.dtos.create_discount_dto import CreateDiscountDTO
from pkg.crm.application.dtos.delete_discount_dto import DeleteDiscountDTO
from pkg.crm.application.dtos.update_discount_dto import UpdateDiscountDTO

from pkg.crm.domain.services.discount_service import (
    DiscountService,
)


@dataclass(frozen=True, slots=True)
class DiscountAdapter:
    discountService: DiscountService


class HttpDiscountAdapter:

    def __init__(self, ctx: DiscountAdapter):
        self.discountService: DiscountService = ctx.discountService

    async def create(self, request: Request) -> JSONResponse:
        try:

            data = await request.json()

            dto: CreateDiscountDTO = CreateDiscountDTO.parse_obj(**data)

            instance = await self.discountService.create(dto=dto)

            return Response(instance)

        except ValidationError as e:
            return ResponseValidationError(content=e)

        except ValueError as e:
            return ResponseValueError(content=e)

    async def get(self, request: Request) -> JSONResponse:
        try:

            id: int = int(request.path_params["id"])

            instance = await self.discountService.get(id=id)

            if not instance:
                return ResponseNotFoundError({"error": "Discount not found"})

            return Response(instance)

        except ValidationError as e:
            return ResponseValidationError(content=e)

        except ValueError as e:
            return ResponseValueError(content=e)

    async def get_all(self, request: Request) -> JSONResponse:

        try:

            dto: PaginateDTO = PaginateDTO(
                limit=int(request.query_params.get("limit") or 100),
                page=int(request.query_params.get("page") or 1),
            )

            instance = await self.discountService.get_all(dto)

            return Response(instance)

        except ValidationError as e:
            return ResponseValidationError(content=e)

        except ValueError as e:
            return ResponseValueError(content=e)

    async def update(self, request: Request) -> JSONResponse:
        try:

            id: int = int(request.path_params["id"])

            data = await request.json()

            data["id"] = id

            dto: UpdateDiscountDTO = UpdateDiscountDTO.parse_obj(data)

            instance = await self.discountService.update(dto=dto)

            return Response(instance)

        except ValidationError as e:
            return ResponseValidationError(content=e)

        except ValueError as e:
            return ResponseValueError(content=e)

    async def delete(self, request: Request) -> JSONResponse:
        try:

            id: int = int(request.path_params["id"])

            dto: DeleteDiscountDTO = DeleteDiscountDTO.parse_obj({"id": id})

            await self.discountService.delete(dto=dto)

            return JSONResponse(status_code=204, content=None)

        except ValueError as e:
            return ResponseValueError(content=e)
