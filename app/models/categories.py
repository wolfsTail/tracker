from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class Categories(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[str] = mapped_column(String(16), default="default")
