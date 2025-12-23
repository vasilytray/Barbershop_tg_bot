from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, Text, ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time, date
# from app.models.masters import Master
from app.dao.database import Base, int_pk, created_at, updated_at, str_uniq, str_null_true

class Specialization(Base):
    # __tablename__ = "specializations" # type: ignore

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[Optional[str]]
    label: Mapped[str]
    specialization: Mapped[str]

    master: Mapped[List["Master"]] = relationship(back_populates="specialization")
    services: Mapped[List["Service"]] = relationship(back_populates="specialization")