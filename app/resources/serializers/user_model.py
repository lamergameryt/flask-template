from app.routes.auth import ns
from flask_restx import fields

UserModel = ns.model(
    "UserModel",
    {
        "id": fields.Integer(required=True),
        "phone": fields.String(required=True),
        "full_name": fields.String(required=True),
        "email": fields.String(required=True),
    },
)
