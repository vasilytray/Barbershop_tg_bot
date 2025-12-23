from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Integer, Text, ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time, date
from app.models.users import User
from app.models.masters import Master
from app.models.services import Service
from app.dao.database import Base, int_pk, created_at, updated_at, str_uniq, str_null_true

class Booking(Base):
    # __tablename__ = "booking" # type: ignore

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    day_booking: Mapped[date] = mapped_column(nullable=False)
    time_booking: Mapped[time] = mapped_column(nullable=False)
    booking_status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),  # Без временной зоны для PostgreSQL
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)  # Убираем временную зону
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),  # Без временной зоны для PostgreSQL
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),  # Убираем временную зону
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None)   # Убираем временную зону
    )

    # Relationships
    master: Mapped["Master"] = relationship(back_populates="bookings")
    service: Mapped["Service"] = relationship(back_populates="bookings")
    user: Mapped["User"] = relationship(back_populates="bookings")