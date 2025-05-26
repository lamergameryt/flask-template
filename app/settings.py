import os
from datetime import timedelta


class Config(object):
    HACKVORTEX_DEBUG = True

    SITE_NAME = os.environ.get("SITE_NAME", "Site Name")
    SWAGGER_DESCRIPTION = os.environ.get("SWAGGER_DESCRIPTION", "Swagger Description")

    FLASK_ADMIN_SWATCH = "minty"

    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", None)


class ProductionConfig(Config):
    HACKVORTEX_DEBUG = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class DevelopmentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=60)

    CORS_ORIGIN_WHITELIST = "*"


configs = {
    "prod": ProductionConfig,
    "dev": DevelopmentConfig,
    "default": DevelopmentConfig,
}
