from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    time_periods: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(16), default="to do")
    category_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)
