from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import TEXT

from ..extensions import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(TEXT, nullable=True)

    @classmethod
    def get_user_by_id(id: int):
        return db.session.execute(db.select(User).where(User.id == id)).scalar_one_or_none()

    @classmethod
    def get_user_by_email(email: str):
        return db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
