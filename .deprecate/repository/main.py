from dataclasses import dataclass
import os

from flask_sqlalchemy import SQLAlchemy
from repository.ClickUpRepository import ClickUpRepository
from repository.CloudflareRepository import CloudflareRepository


@dataclass(frozen=True)
class Repository:
    ClickUpRepo: ClickUpRepository
    CloudflareRepo: CloudflareRepository


class NewRepository:
    db: SQLAlchemy

    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def init(self) -> Repository:
        CLICKUP_CODE: str = os.getenv("CLICKUP_CODE")
        CLICKUP_TOKEN: str = os.getenv("CLICKUP_TOKEN")

        clickup_repo: ClickUpRepository = ClickUpRepository(
            client_id=os.getenv("CLICKUP_CLIENT_ID"),
            client_secret=os.getenv("CLICKUP_CLIENT_SECRET"),
            redirect_uri="https://api.onbbu.ar",
        )

        clickup_repo.set_token(token=CLICKUP_TOKEN)

        cloudflare_repo: CloudflareRepository = CloudflareRepository(
            api_token=os.getenv("CLOUDFLARE_TOKEN"),
            zone_id=os.getenv("CLOUDFLARE_ZONE"),
        )

        return Repository(ClickUpRepo=clickup_repo, CloudflareRepo=cloudflare_repo)
