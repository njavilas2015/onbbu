from models.ClickupModel import ItemFolder, ItemList, ItemSpaces, ItemTeams, ItemTask, ItemWebhooks
from repository.ClickUpRepository import ClickUpRepository


class ClickUpService:
    repo: ClickUpRepository

    def __init__(self, repo: ClickUpRepository):
        self.repo = repo

    def get_teams(self) -> list[ItemTeams]:
        return self.repo.get_teams()

    def get_spaces(self, team_id: int) -> list[ItemSpaces]:
        return self.repo.get_spaces(team_id=team_id)

    def get_folders(self, space_id: int) -> list[ItemFolder]:
        return self.repo.get_folders(space_id=space_id)

    def get_space_lists(self, space_id: int) -> list[ItemList]:
        return self.repo.get_space_lists(space_id=space_id)

    def get_folder_lists(self, folder_id: int) -> list[ItemList]:
        return self.repo.get_folder_lists(folder_id=folder_id)

    def get_tasks(self, list_id: int) -> list[ItemTask]:
        return self.repo.get_tasks(list_id=list_id)

    def list_hooks(self, team_id: int) -> list[ItemWebhooks]:
        return self.repo.list_hooks(team_id=team_id)

    def create_hooks(self, team_id: int, endpoint: str, events: list[str]):
        return self.repo.create_hooks(team_id=team_id, endpoint=endpoint, events=events)
    
    def destroy_hooks(self, webhook_id: int) -> str:
        return self.repo.destroy_hooks(webhook_id=webhook_id)
