from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, Text, ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time, date
# from app.models.bookings import Booking
from app.dao.database import Base, int_pk, created_at, updated_at, str_uniq, str_null_true


class User(Base):
    # __tablename__ = "users" # type: ignore
    id: Mapped[int_pk]
    # id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    username: Mapped[str] = mapped_column(index=True, nullable=True)
    first_name: Mapped[str] = mapped_column(index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(index=True, nullable=True)
    user_phone: Mapped[str_uniq] #= mapped_column(String, unique=True, index=True, nullable=False)

    # Relationships
    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")