from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, Text, ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time, date
from app.models.bookings import Booking
from app.models.specializations import Specialization
from app.dao.database import Base, int_pk, created_at, updated_at, str_uniq, str_null_true

class Master(Base):
    # __tablename__ = "masters" # type: ignore

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(index=True, nullable=True)
    patronymic: Mapped[Optional[str]]
    special: Mapped[str]
    specialization_id: Mapped[int] = mapped_column(ForeignKey("specializations.id"), server_default=text("1"))
    work_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    experience: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    photo: Mapped[str]

    # Relationships
    bookings: Mapped[List["Booking"]] = relationship(back_populates="doctor")

    specialization: Mapped["Specialization"] = relationship("Specialization", back_populates="doctors",
                                                            lazy="joined")