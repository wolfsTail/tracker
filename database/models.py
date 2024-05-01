from sqlalchemy import Integer, String
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


class Categories(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64))