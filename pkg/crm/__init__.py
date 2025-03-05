from dataclasses import dataclass

from onbbu import ServerHttp

from pkg.crm.domain.services.main import ServiceRegistry, NewService, ServicesContext

from pkg.crm.infrastructure.adapters.main import (
    ConfigHttpAdapter,
    NewHttpAdapter,
)

from pkg.crm.infrastructure.persistence.repositories.main import (
    NewRepository,
    Repository,
)


@dataclass(frozen=True, slots=True)
class ConfigInit:
    http: ServerHttp


class Module:
    config: ConfigInit

    def __init__(self, config: ConfigInit):

        self.config = config

    def init(self) -> ServiceRegistry:

        repo: Repository = NewRepository().init()

        service: ServiceRegistry = NewService(ctx=ServicesContext(Repo=repo)).init()

        NewHttpAdapter(
            ConfigHttpAdapter(
                Http=self.config.http,
                discountService=service.discountService,
            )
        )

        return service
