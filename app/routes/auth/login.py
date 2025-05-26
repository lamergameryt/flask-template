from flask import current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy import exc

from app.extensions import CustomParser, db, limiter
from app.models.user import User
from app.resources.serializers.user_model import UserModel

from . import create_tokens, ns


@ns.route("/login")
class LoginRoute(Resource):
    _login_parser = CustomParser()
    _login_parser.add_argument("token", type=str)

    @ns.expect(_login_parser)
    @ns.marshal_with(UserModel)
    @limiter.limit("10/hour")
    @ns.doc(description="Authenticate a user with the specified Google token.")
    def post(self):
        args = self._login_parser.parse_args(strict=True)

        CLIENT_ID = current_app.config.get("CLIENT_ID")

        idinfo = id_token.verify_oauth2_token(args["token"], requests.Request())
        if idinfo["aud"] != CLIENT_ID:
            return ns.abort(400, "Invalid user credentials entered.")

        user = User.get_user_by_email(idinfo.get("email"))
        if not user:
            user = User()

            user.full_name = idinfo.get("name")
            user.email = idinfo.get("email")

            try:
                db.session.add(user)
                db.session.commit()
            except exc.SQLAlchemyError as _:
                return ns.abort(400, f"Error: Could not create new user for {user.email}")

        access_token, refresh_token = create_tokens(user, True)

        user.access_token = access_token
        user.refresh_token = refresh_token

        return user
