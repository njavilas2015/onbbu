import json
import requests
from requests import Response
from models.CloudflareModel import DNSRecord


class CloudflareRepository:
    api_token: str
    zone_id: int

    def __init__(self, api_token: str, zone_id: int):
        self.api_token = api_token

        self.zone_id = zone_id

        self.base_url = "https://api.cloudflare.com/client/v4"

        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def verify(self) -> str:

        url: str = f"{self.base_url}/user/tokens/verify"

        response: Response = requests.get(url, headers=self.headers)

        if response.status_code == 200:

            data = response.json()

            return data.get("messages")[0]["message"]

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_subdomains(self) -> list[DNSRecord]:

        url: str = f"{self.base_url}/zones/{self.zone_id}/dns_records?type=A"

        response: Response = requests.get(url, headers=self.headers)

        if response.status_code == 200:

            data = response.json()

            return [
                DNSRecord(
                    id=item["id"],
                    name=item["name"],
                    comment=item["comment"],
                    content=item["content"],
                    created_on=item["created_on"],
                    modified_on=item["modified_on"],
                    proxied=item["proxied"],
                    record_type=item["type"],
                    ttl=item["ttl"],
                )
                for item in data.get("result", [])
            ]

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def create_dns_record(self, subdomain: str, ip: str, base_domain: str) -> DNSRecord:

        url: str = f"{self.base_url}/zones/{self.zone_id}/dns_records"

        data = {
            "type": "A",
            "name": f"{subdomain}.{base_domain}",
            "content": ip,
            "ttl": 120,
            "proxied": False,
        }

        response: Response = requests.post(
            url, headers=self.headers, data=json.dumps(data)
        )

        if response.status_code == 200:

            data = response.json()

            item = data.get("result")

            return DNSRecord(
                id=item["id"],
                name=item["name"],
                comment=item["comment"],
                content=item["content"],
                created_on=item["created_on"],
                modified_on=item["modified_on"],
                proxied=item["proxied"],
                record_type=item["type"],
                ttl=item["ttl"],
            )

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def delete_dns_record(self, record_id: str) -> str:

        url: str = f"{self.base_url}/zones/{self.zone_id}/dns_records/{record_id}"

        response: Response = requests.delete(url, headers=self.headers)

        if response.status_code == 200:
            return "deleted"

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
