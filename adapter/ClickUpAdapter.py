from dataclasses import dataclass, asdict
from flask import jsonify, request

from service.ClickUpService import ClickUpService
from service.CICDService import CICDService


@dataclass(frozen=True)
class ClickUpAdapter:
    ClickUpService: ClickUpService
    CICDService: CICDService


class HttpClickUpAdapter:
    ctx: ClickUpAdapter

    def __init__(self, ctx: ClickUpAdapter):
        self.ctx = ctx

    def webhook(self):
        try:

            data = request.get_json()

            event = data.get("event")

            if event == "taskCreated":
                self.ctx.CICDService.taskCreated()

            if event == "taskUpdated":
                self.ctx.CICDService.taskUpdated()

            if event == "taskDeleted":
                self.ctx.CICDService.taskDeleted()

            if event == "taskMoved":
                self.ctx.CICDService.taskMoved()

            else:
                print(f"📢 Evento recibido: {event}")
                print(f"📦 Datos: {data}")

            return jsonify({"status": "Webhook recibido correctamente"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_teams(self):
        try:

            data = self.ctx.ClickUpService.get_teams()

            return jsonify([asdict(item) for item in data]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_spaces(self):
        try:

            team_id = request.args.get("team")

            data = self.ctx.ClickUpService.get_spaces(team_id=team_id)

            return jsonify([asdict(item) for item in data]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_folders(self):
        try:

            space_id = request.args.get("space")

            data = self.ctx.ClickUpService.get_folders(space_id=space_id)

            return jsonify([asdict(item) for item in data]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_space_lists(self):
        try:

            space_id = request.args.get("space")

            data = self.ctx.ClickUpService.get_space_lists(space_id=space_id)

            return jsonify([asdict(item) for item in data]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_folder_lists(self):
        try:

            folder_id = request.args.get("folder")

            data = self.ctx.ClickUpService.get_folder_lists(folder_id=folder_id)

            return jsonify([asdict(item) for item in data]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_tasks(self):
        try:

            list_id = request.args.get("list")

            data = self.ctx.ClickUpService.get_tasks(list_id=list_id)

            return jsonify([asdict(item) for item in data]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def list_hooks(self):
        try:

            team_id = request.args.get("team")

            data = self.ctx.ClickUpService.list_hooks(team_id=team_id)

            return jsonify([asdict(item) for item in data]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    def destroy_hooks(self):
        try:

            webhook_id = request.args.get("webhook")

            data = self.ctx.ClickUpService.destroy_hooks(webhook_id=webhook_id)

            return jsonify(data), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def create_hooks(self):
        try:

            data = request.get_json()

            team_id = data.get("team")

            endpoint = data.get("endpoint")

            events = data.get("events")

            if not team_id or not endpoint or not events:
                return jsonify({"error": "Missing parameters"}), 400

            data = self.ctx.ClickUpService.create_hooks(
                team_id=team_id, endpoint=endpoint, events=events
            )

            return jsonify([asdict(item) for item in data]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
