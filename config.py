import os
import json
import connexion
from db import init_db
from dotenv import load_dotenv
from marshmallow import ValidationError
from flask import Response


load_dotenv()


class Config(object):
    TESTING = False
    DEBUG = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def DATABASE_URI(self):
        return f"sqlite:///{self.DB_SERVER}"


class ProductionConfig(Config):
    DB_SERVER = "db.sqlite3"


class TestingConfig(Config):
    DB_SERVER = ":memory:"
    DEBUG = True
    TESTING = True


def render_validation_error(error):
    return Response(
        response=json.dumps(error.messages), status=400, mimetype="application/json"
    )


conn_app = connexion.App(__name__, specification_dir="./")
conn_app.add_error_handler(ValidationError, render_validation_error)

app = conn_app.app

if os.environ.get("ENV") == "production":
    settings = ProductionConfig()
else:
    settings = TestingConfig()
app.config.from_object(settings)

db = init_db(settings.DATABASE_URI)
