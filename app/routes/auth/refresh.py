from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
from sqlalchemy import exc

from app.extensions import limiter
from app.models.user import User
from app.resources.serializers.user_model import UserModel

from . import create_tokens, ns


@ns.route("/refresh")
class RefreshRoute(Resource):
    @ns.marshal_with(UserModel)
    @limiter.limit("10/hour")
    @jwt_required(refresh=True)
    @ns.doc(description="Generate a new access token using the refresh token of a user.")
    def post(self):
        identity = get_jwt_identity()
        try:
            user = User.get_user_by_id(identity)
        except exc.SQLAlchemyError as _:
            return ns.abort(400, f"Error: Could not find user with id {identity}.")

        if not user:
            return ns.abort(400, f"Error: Could not find user with id {identity}.")

        access_token = create_tokens(user)
        user.access_token = access_token
        return user
