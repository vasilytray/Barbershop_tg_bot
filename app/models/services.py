# app/models/services.py
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from sqlalchemy import Integer, Text, ForeignKey, DateTime, text, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.masters import Master
from app.models.specializations import Specialization
from app.dao.database import Base, int_pk, created_at, updated_at, str_uniq, str_null_true


class Service(Base):
    # __tablename__ = "services" # type: ignore
    
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(index=True, nullable=False)  # Название услуги
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Описание услуги
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)  # Продолжительность в минутах
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)  # Цена услуги
    
    # Связи с другими таблицами
    master_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("masters.id", ondelete="CASCADE"), 
        nullable=True
    )  # Если услуга привязана к конкретному мастеру
    
    specialization_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("specializations.id", ondelete="CASCADE"), 
        nullable=True
    )  # Если услуга привязана к специализации
    
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    # Relationships
    master: Mapped[Optional["Master"]] = relationship("Master", back_populates="services")
    specialization: Mapped[Optional["Specialization"]] = relationship(
        "Specialization", 
        back_populates="services"
    )
    bookings: Mapped[List["Booking"]] = relationship(back_populates="service")