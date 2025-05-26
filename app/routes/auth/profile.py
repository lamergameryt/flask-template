from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
from sqlalchemy import exc

from app.extensions import CustomParser, db
from app.models.user import User
from app.resources.serializers.user_model import UserModel

from . import ns


@ns.route("/profile")
class ProfileRoute(Resource):
    _profile_parser = CustomParser()
    _profile_parser.add_argument("full_name", type=str)
    _profile_parser.add_argument("phone", type=str)

    @ns.expect(_profile_parser)
    @ns.marshal_with(UserModel)
    @ns.doc(description="Route to update user profile details.")
    @jwt_required()
    def put(self):
        args = self._profile_parser.parse_args(strict=True)
        identity = get_jwt_identity()
        try:
            user = User.get_user_by_id(identity)
        except exc.SQLAlchemyError as _:
            return ns.abort(400, f"Error: Could not find user with id {identity}.")

        if not user:
            return ns.abort(400, f"Error: Could not find user with id {identity}.")

        user.full_name = args.get("full_name")
        user.phone = args.get("phone")

        db.session.commit()

        return user
