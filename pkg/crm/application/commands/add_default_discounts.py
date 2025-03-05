from onbbu import BaseCommand, register_command


@register_command
class Command(BaseCommand):
    """Command to run the FastAPI server."""
    
    name: str = "add_default_discounts"
    help: str = "Crear descuentos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--host", type=str, default="0.0.0.0", help="Host for the server"
        )
        parser.add_argument(
            "--port", type=int, default=8000, help="Port for the server"
        )

    def handle(self, args):
        print(f"🚀 Starting server on {args.host}:{args.port}...")
        # uvicorn.run("crm.infrastructure.server:app", host=args.host, port=args.port)
