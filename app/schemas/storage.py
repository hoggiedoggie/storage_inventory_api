from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class StorageBase(BaseModel):
    model: str
    serial_number: str
    capacity_gb: int
    status: Optional[str] = "active"

class StorageCreate(StorageBase):
    pass

class StorageUpdate(BaseModel):
    model: Optional[str] = None
    serial_number: Optional[str] = None
    capacity_gb: Optional[int] = None
    status: Optional[str] = None

class StorageResponse(StorageBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class StorageListResponse(BaseModel):
    data: List[StorageResponse]
    meta: dict