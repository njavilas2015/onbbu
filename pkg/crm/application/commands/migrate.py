import asyncio
from onbbu import BaseCommand, register_command, DatabaseManager

from internal.settings import INSTALLED_APPS


@register_command
class Command(BaseCommand):
    """Command to run database migrations."""

    name: str = "migrate"
    help: str = "Run database migrations"

    def handle(self, args):
        print("🔄 Running database migrations...")

        db_manager = DatabaseManager(INSTALLED_APPS)

        try:
            asyncio.run(db_manager.run())
        except KeyboardInterrupt:
            print("🚨 Interrupción detectada. Finalizando...")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
