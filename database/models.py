from typing import Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    time_periods: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(16), default="to do")
    category_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)


class Categories(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[str] = mapped_column(String(16), default="default")


class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), nullable=True)
    password: Mapped[str] = mapped_column(String(128), nullable=True)
    google_access_token: Mapped[Optional[str]]
    yandex_access_token: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
