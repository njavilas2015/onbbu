from server import server
from flask_sqlalchemy import SQLAlchemy

server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'

server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db: SQLAlchemy = SQLAlchemy(server)