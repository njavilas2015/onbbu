import requests
from requests import Response
from models.ClickupModel import ItemFolder, ItemTask, ItemTeams, ItemSpaces, ItemList, ItemWebhooks
from tools.convert import ms_to_date


class ClickUpRepository:
    BASE_URL: str
    client_id: str
    client_secret: str
    redirect_uri: str
    access_token: str | None
    refresh_token: str | None
    headers: dict[str, str]

    def __init__(self, client_id, client_secret: str, redirect_uri: str):

        self.client_id = client_id

        self.client_secret = client_secret

        self.redirect_uri = redirect_uri

        self.access_token = None

        self.refresh_token = None

        self.headers = {}

        self.BASE_URL = "https://api.clickup.com/api/v2"

    def auth(self, authorization_code: str):
        """
        Get a new access_token using authorization code
        https://app.clickup.com/api?client_id=TOFCNWCMPNFD4ZV8YA61TH48ZGC8F29Z&redirect_uri=https:%2F%2Fapi.onbbu.ar
        """

        url: str = f"{self.BASE_URL}/oauth/token"

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(url, data)

        if response.status_code == 200:

            data = response.json()

            self.access_token = data.get("access_token")

            self.refresh_token = data.get("refresh_token")

            self.headers = {"Authorization": f"Bearer {self.access_token}"}

            print("Acceso concedido. Access Token:", self.access_token)
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def set_token(self, token: str):
        self.headers = {"Authorization": f"Bearer {token}"}

    def auth_refresh_token(self):
        """Renovar el access_token usando el refresh_token"""

        url: str = f"{self.BASE_URL}/oauth/token"

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }

        response = requests.post(url, data)

        if response.status_code == 200:

            data = response.json()

            self.access_token = data.get("access_token")

            self.refresh_token = data.get("refresh_token")

            self.headers = {"Authorization": f"Bearer {self.access_token}"}

            print("Token renovado. Nuevo Access Token:", self.access_token)
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_tasks(self, list_id: int) -> list[ItemTask]:

        url: str = f"{self.BASE_URL}/list/{list_id}/task?include_closed=true"

        response: Response = requests.get(url, headers=self.headers)

        if response.status_code == 200:

            data = response.json()

            return [
                ItemTask(
                    id=task["id"],
                    name=task["name"],
                    description=task["text_content"],
                    tags=[x["name"] for x in task["tags"]],
                    status=task["status"]["status"],
                    assignee=task.get("assignees", []),
                    priority=(
                        task["priority"]["priority"]
                        if task["priority"] is not None
                        else None
                    ),
                    due_date=ms_to_date(task["due_date"]),
                    start_date=ms_to_date(task["start_date"]),
                    points=task["points"],
                    time_estimate=ms_to_date(task["time_estimate"]),
                    custom_fields=task["custom_fields"],
                    dependencies=task["dependencies"],
                    linked_tasks=task["linked_tasks"],
                    date_created=ms_to_date(task["date_created"]),
                    date_updated=ms_to_date(task["date_updated"]),
                    date_closed=ms_to_date(task["date_closed"]),
                    date_done=ms_to_date(task["date_done"]),
                )
                for task in data.get("tasks", [])
            ]
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_space_lists(self, space_id: int):

        url: str = f"{self.BASE_URL}/space/{space_id}/list"

        response: Response = requests.get(url, headers=self.headers)

        if response.status_code == 200:

            data = response.json()

            return [
                ItemList(id=list["id"], name=list["name"])
                for list in data.get("lists", [])
            ]

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_folder_lists(self, folder_id: int):

        url: str = f"{self.BASE_URL}/folder/{folder_id}/list"

        response: Response = requests.get(url, headers=self.headers)

        if response.status_code == 200:

            data = response.json()

            return [
                ItemList(id=list["id"], name=list["name"])
                for list in data.get("lists", [])
            ]

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_spaces(self, team_id: int) -> list[ItemSpaces]:

        url: str = f"{self.BASE_URL}/team/{team_id}/space"

        response: Response = requests.get(url, headers=self.headers)

        if response.status_code == 200:

            data = response.json()

            return [
                ItemSpaces(id=team["id"], name=team["name"])
                for team in data.get("spaces", [])
            ]

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_folders(self, space_id: int) -> list[ItemFolder]:

        url: str = f"{self.BASE_URL}/team/{space_id}/folder"

        response: Response = requests.get(url, headers=self.headers)

        if response.status_code == 200:

            data = response.json()

            return [
                ItemFolder(id=team["id"], name=team["name"])
                for team in data.get("folders", [])
            ]

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_teams(self) -> list[ItemTeams]:

        url: str = f"{self.BASE_URL}/team"

        response: Response = requests.get(url, headers=self.headers)

        if response.status_code == 200:

            data = response.json()

            return [
                ItemTeams(id=team["id"], name=team["name"])
                for team in data.get("teams", [])
            ]

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
    def destroy_hooks(self, webhook_id: int):

        url: str = f'{self.BASE_URL}/webhook/{webhook_id}'

        response: Response = requests.delete(url, headers=self.headers)

        if response.status_code == 200:
            return "deleted"

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def list_hooks(self, team_id: int):

        url: str = f'{self.BASE_URL}/team/{team_id}/webhook'

        response: Response = requests.get(url, headers=self.headers)

        if response.status_code == 200:

            data = response.json()

            return [
                ItemWebhooks(
                    id=item["id"], 
                    endpoint=item["endpoint"],
                    events=item["events"],
                )
                for item in data.get("webhooks", [])
            ]

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
    def create_hooks(self, team_id: int, events: list[str], endpoint: str):
        """
        {
            'id': '63bba101-a4cb-4ac9-8f16-a2683e4e40ca', 
            'webhook': {
                'id': '63bba101-a4cb-4ac9-8f16-a2683e4e40ca', 
                'userid': 114291412, 
                'team_id': 9011726685, 
                'endpoint': 'https://838f-181-81-32-75.ngrok-free.app/webhook', 
                'client_id': 'TOFCNWCMPNFD4ZV8YA61TH48ZGC8F29Z', 
                'events': ['taskCreated', 'taskUpdated', 'taskDeleted'], 
                'task_id': None, 
                'list_id': None, 
                'folder_id': None, 
                'space_id': None, 
                'view_id': None,
                'health': {
                    'status': 'active', 
                    'fail_count': 0
                }, 
                'secret': 'MXZS7B92WDI6TXFLQQTX3D3IUV4QWF7XNO19108E0VP57M2WUF8DP77ATK4HBZXB'
            }
        }
        """

        url: str = f'{self.BASE_URL}/team/{team_id}/webhook'

        payload = {
            "endpoint": endpoint,
            "events": events
        }

        response: Response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 200:

            data = response.json()

            print(data)
            
            return [
                #ItemTeams(id=team["id"], name=team["name"])
                #for team in data.get("teams", [])
            ]

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
