import os

from dotenv import load_dotenv
from flask import Blueprint, Flask

from .admin.views import CustomAdminIndexView
from .extensions import admin, api, cors, db, jwt, limiter, migrate
from .routes import auth
from .routes.errors import views as error_views
from .settings import configs


def create_app(*args, **kwargs):
    load_dotenv()

    app_env = os.environ.get("APP_ENVIRONMENT", "default")

    app = Flask(__name__)
    app.config.from_object(obj=configs[app_env])
    app.url_map.strict_slashes = False

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    cors.init_app(app)
    limiter.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    admin._set_admin_index_view(CustomAdminIndexView())
    admin.init_app(app)


def register_blueprints(app):
    origins = app.config.get("CORS_ORIGIN_WHITELIST")
    if not origins:
        raise ValueError(
            "Error: 'CORS_ORIGIN_WHITELIST' variable doesn't exist within configuration."
        )

    cors.init_app(app, origins=origins)

    api.add_namespace(auth.ns)

    blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

    DEBUG = app.config.get("HACKVORTEX_DEBUG", False)
    api.init_app(blueprint, add_specs=DEBUG, doc=DEBUG)

    app.register_blueprint(blueprint)
    app.register_blueprint(error_views.blueprint)
