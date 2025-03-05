from models.CloudflareModel import DNSRecord
from repository.CloudflareRepository import CloudflareRepository


class CloudflareService:
    repo: CloudflareRepository

    def __init__(self, repo: CloudflareRepository):
        self.repo = repo

    def verify_token(self) -> str:
        """
        Check if the Cloudflare API token is valid.
        """
        return self.repo.verify()

    def get_subdomains(self) -> list[DNSRecord]:
        return self.repo.get_subdomains()

    def create_subdomain(self, subdomain: str, ip: str, base_domain: str) -> DNSRecord:
        """
        Create a subdomain on Cloudflare.

        :param subdomain: Name of the subdomain (without the base domain).
        :param ip: IP address to which the subdomain will point.
        :param base_domain: Base domain (example: 'yourdomain.com').
        :return: Cloudflare API response.
        """
        return self.repo.create_dns_record(subdomain, ip, base_domain)

    def delete_subdomain(self, record_id: str) -> str:
        """
        Delete a subdomain in Cloudflare.

        :param subdomain: Name of the subdomain (without the base domain).
        :param base_domain: Base domain (example: 'yourdomain.com').
        :return: Cloudflare API response.
        """
        return self.repo.delete_dns_record(record_id=record_id)
