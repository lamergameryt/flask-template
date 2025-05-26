from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import Namespace

from app.models.user import User

ns = Namespace("auth", description="Authentication related endpoints")


def create_tokens(user: User, include_refresh: bool = False):
    access_token = create_access_token(user.id)

    if include_refresh:
        return access_token, create_refresh_token(user.id)
    else:
        return access_token


from . import login, profile, refresh
