from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), nullable=True)
    password: Mapped[str] = mapped_column(String(128), nullable=True)
    google_access_token: Mapped[Optional[str]]
    yandex_access_token: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
