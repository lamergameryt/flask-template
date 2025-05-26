import os

from flask import request
from flask_admin import Admin
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_migrate import Migrate
from flask_restx import Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from .settings import configs


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


config_name = os.environ.get("APP_ENVIRONMENT", "default")
config = configs.get(config_name)

admin = Admin(
    name=config.SITE_NAME,
)

db = SQLAlchemy(model_class=Base)
cors = CORS()
jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(lambda: request.access_route[-1], default_limits=["1000/day", "50/hour"])

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}
api = Api(
    version="1.0",
    description=config.SWAGGER_DESCRIPTION,
    authorizations=authorizations,
    security="Bearer",
)


class CustomParser(reqparse.RequestParser):
    class _Argument(reqparse.Argument):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.required = kwargs.get("required", True)
            self.location = kwargs.get("location", "json")
            self.trim = kwargs.get("trim", True)

    def __init__(self, *args, **kwargs):
        self.default_location = kwargs.pop("default_location", None)

        super().__init__(*args, **kwargs)
        self.argument_class = self._Argument

    def add_argument(self, *args, **kwargs):
        if self.default_location and isinstance(self.default_location, (str, list)):
            kwargs["location"] = self.default_location

        return super().add_argument(*args, **kwargs)


class FakeRequest(dict):
    def __init__(self, data: dict = None):
        self.json = data

    def get_json(self, *args, **kwargs):
        return self.json

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
