from dotenv import load_dotenv

load_dotenv()

from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

from server import server
from orm.main import db
from service.main import Context, ModuleContext, NewService
from repository.main import NewRepository
from adapter.main import NewHttpAdapter, ConfigHttpAdapter


@dataclass(frozen=True)
class ConfigInit:
    db: SQLAlchemy


def init(config: ConfigInit) -> ModuleContext:

    repo = NewRepository(db=config.db)

    service = NewService(ctx=Context(repo=repo.init()))

    return service.init()

if __name__ == "__main__":

    service = init(config=ConfigInit(db=db))

    http_adapter = NewHttpAdapter(config=ConfigHttpAdapter(
        CloudflareService=service.CloudflareService,
        ClickUpService=service.ClickUpService,
        CICDService=service.CICDService,
        Http=server
    ))

    http_adapter.init()

    server.run(port=5000, debug=True)
