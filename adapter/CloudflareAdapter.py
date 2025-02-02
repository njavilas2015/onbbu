from dataclasses import asdict, dataclass
from flask import jsonify, request
from service.CloudflareService import CloudflareService


@dataclass(frozen=True)
class CloudflareAdapter:
    CloudflareService: CloudflareService


class HttpCloudflareAdapter:
    ctx: CloudflareAdapter

    def __init__(self, ctx: CloudflareAdapter):
        self.ctx = ctx

    def verify_token(self):
        try:

            data = self.ctx.CloudflareService.verify_token()

            return jsonify(data), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_subdomains(self):
        try:

            data = self.ctx.CloudflareService.get_subdomains()

            return jsonify([asdict(item) for item in data]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def create_subdomain(self):
        try:
            data = request.get_json()

            subdomain = data.get("subdomain")
            ip = data.get("ip")
            base_domain = data.get("base_domain")

            if not subdomain or not ip or not base_domain:
                return jsonify({"error": "Missing parameters"}), 400

            data = self.ctx.CloudflareService.create_subdomain(
                subdomain, ip, base_domain
            )

            return jsonify(asdict(data)), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete_subdomain(self):
        try:

            record_id = request.args.get("record")

            if not record_id:
                return jsonify({"error": "Missing parameters"}), 400

            response = self.ctx.CloudflareService.delete_subdomain(record_id)

            return jsonify(response), 204

        except Exception as e:
            return jsonify({"error": str(e)}), 500
