from dataclasses import dataclass
from repository.main import Repository
from service.CloudflareService import CloudflareService
from service.ClickUpService import ClickUpService
from service.CICDService import CICDService


@dataclass(frozen=True)
class ModuleContext:
    ClickUpService: ClickUpService
    CloudflareService: CloudflareService
    CICDService: CICDService


@dataclass(frozen=True)
class Context:
    repo: Repository


class NewService:
    ctx: Context

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    def init(self) -> ModuleContext:

        clickup_service: ClickUpService = ClickUpService(repo=self.ctx.repo.ClickUpRepo)

        cloudflare_service: CloudflareService = CloudflareService(
            repo=self.ctx.repo.CloudflareRepo
        )

        cicd_service: CICDService = CICDService(
            cloudflareService=self.ctx.repo.CloudflareRepo,
            clickUpService=self.ctx.repo.ClickUpRepo,
        )

        return ModuleContext(
            ClickUpService=clickup_service,
            CloudflareService=cloudflare_service,
            CICDService=cicd_service,
        )
