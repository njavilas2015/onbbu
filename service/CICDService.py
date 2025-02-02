from service.ClickUpService import ClickUpService
from service.CloudflareService import CloudflareService


class CICDService:
    cloudflareService: CloudflareService
    clickUpService: ClickUpService

    def __init__(
        self, cloudflareService: CloudflareService, clickUpService: ClickUpService
    ):
        self.cloudflareService = cloudflareService
        self.clickUpService = clickUpService

    def create_task(self, data) -> None:
        """
        1 - Si el card está asociada al area de desarrollo debe crearse un issues en git
        2 - Crear hilo en discord para notificar
        3 - ?
        """
        pass

    def update_task(self) -> None:
        pass

    def delete_task(self) -> None:
        pass
