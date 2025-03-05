from onbbu import create_app, ServerHttp
from pkg.crm import Module as CRM

server: ServerHttp = create_app(port=8000)

crm = CRM(server.config).init()