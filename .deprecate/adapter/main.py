from dataclasses import dataclass
from flask import Blueprint, Flask

from service.ClickUpService import ClickUpService
from service.CloudflareService import CloudflareService
from service.CICDService import CICDService

from adapter.ClickUpAdapter import ClickUpAdapter, HttpClickUpAdapter
from adapter.CloudflareAdapter import CloudflareAdapter, HttpCloudflareAdapter

@dataclass(frozen=True)
class ConfigHttpAdapter:
    Http: Flask
    ClickUpService: ClickUpService
    CloudflareService: CloudflareService
    CICDService: CICDService


class NewHttpAdapter:
    config: ConfigHttpAdapter

    def __init__(self, config: ConfigHttpAdapter) -> None:
        self.config = config

    def init(self) -> None:

        clickupAdapter = HttpClickUpAdapter(
            ctx=ClickUpAdapter(ClickUpService=self.config.ClickUpService)
        )

        clickupGroup = Blueprint(name="clickup", import_name=__name__)

        clickupGroup.add_url_rule(
            "/webhook", view_func=clickupAdapter.webhook, methods=["POST"]
        )

        clickupGroup.add_url_rule(
            "/teams", view_func=clickupAdapter.get_teams, methods=["GET"]
        )

        clickupGroup.add_url_rule(
            "/spaces", view_func=clickupAdapter.get_spaces, methods=["GET"]
        )

        clickupGroup.add_url_rule(
            "/folders", view_func=clickupAdapter.get_folders, methods=["GET"]
        )

        clickupGroup.add_url_rule(
            "/space-lists", view_func=clickupAdapter.get_space_lists, methods=["GET"]
        )

        clickupGroup.add_url_rule(
            "/folder-lists", view_func=clickupAdapter.get_folder_lists, methods=["GET"]
        )

        clickupGroup.add_url_rule(
            "/tasks", view_func=clickupAdapter.get_tasks, methods=["GET"]
        )

        clickupGroup.add_url_rule(
            "/hooks", view_func=clickupAdapter.list_hooks, methods=["GET"]
        )

        clickupGroup.add_url_rule(
            "/hooks", view_func=clickupAdapter.create_hooks, methods=["POST"]
        )

        clickupGroup.add_url_rule(
            "/hooks", view_func=clickupAdapter.destroy_hooks, methods=["DELETE"]
        )

        self.config.Http.register_blueprint(clickupGroup, url_prefix="/clickup")


        cloudflareAdapter = HttpCloudflareAdapter(
            ctx=CloudflareAdapter(CloudflareService=self.config.CloudflareService)
        )
        
        cloudflareGroup = Blueprint(name="cloudflare", import_name=__name__)

        cloudflareGroup.add_url_rule(
            "/subdomain", view_func=cloudflareAdapter.create_subdomain, methods=["POST"]
        )

        cloudflareGroup.add_url_rule(
            "/subdomain", view_func=cloudflareAdapter.delete_subdomain, methods=["DELETE"]
        )

        cloudflareGroup.add_url_rule(
            "/subdomain", view_func=cloudflareAdapter.get_subdomains, methods=["GET"]
        )

        self.config.Http.register_blueprint(cloudflareGroup, url_prefix="/cloudflare")
