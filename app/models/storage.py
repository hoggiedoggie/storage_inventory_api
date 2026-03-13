import uuid
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base

class StorageDevice(Base):
    __tablename__ = "storage_devices"

    # Первичный ключ 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Содержательные поля (WD/Seagate)
    model = Column(String, nullable=False)           # "Western Digital Blue"
    serial_number = Column(String, unique=True)      # Серийник уникален
    capacity_gb = Column(Integer, nullable=False)    # Объем в ГБ
    status = Column(String, default="active")        # Статус: active, faulty, replacement
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Реализация Soft Delete
    # Если тут NULL - диск в строю. Если дата - диск считается "удаленным"
    deleted_at = Column(DateTime(timezone=True), nullable=True)