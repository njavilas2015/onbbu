from dataclasses import dataclass

from onbbu import ServerHttp, HTTPMethod, RouterHttp


from pkg.crm.infrastructure.adapters.adapter_discounts_http import (
    HttpDiscountAdapter,
    DiscountAdapter,
)

from pkg.crm.domain.services.discount_service import (
    DiscountService,
)


@dataclass(frozen=True, slots=True)
class ConfigHttpAdapter:
    Http: ServerHttp
    discountService: DiscountService


class NewHttpAdapter:

    def __init__(self, config: ConfigHttpAdapter):

        discountAdapter: HttpDiscountAdapter = HttpDiscountAdapter(
            DiscountAdapter(discountService=config.discountService)
        )

        router: RouterHttp = RouterHttp(prefix="/crm")

        router.add_route(
            path="/discounts/{id}",
            method=HTTPMethod.GET,
            endpoint=discountAdapter.get,
        )

        router.add_route(
            path="/discounts",
            method=HTTPMethod.GET,
            endpoint=discountAdapter.get_all,
        )

        router.add_route(
            path="/discounts",
            method=HTTPMethod.POST,
            endpoint=discountAdapter.create,
        )

        router.add_route(
            path="/discounts/{id}",
            method=HTTPMethod.PUT,
            endpoint=discountAdapter.update,
        )

        router.add_route(
            path="/discounts/{id}",
            method=HTTPMethod.DELETE,
            endpoint=discountAdapter.delete,
        )

        config.Http.include_router(router)
