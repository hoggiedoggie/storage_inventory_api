from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.services.storage import storage_service
from app.schemas.storage import (
    StorageCreate, 
    StorageUpdate, 
    StorageResponse, 
    StorageListResponse
)

router = APIRouter()

# 1. Get list (GET /)
@router.get("/", response_model=StorageListResponse)
def read_devices(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    items, total = storage_service.get_multi(db, page=page, limit=limit)
    
    # Calculate total pages for metadata
    total_pages = (total + limit - 1) // limit
    
    return {
        "data": items,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "totalPages": total_pages
        }
    }

# 2. Create new disk (POST /)
@router.post("/", response_model=StorageResponse, status_code=status.HTTP_201_CREATED)
def create_device(obj_in: StorageCreate, db: Session = Depends(get_db)):
    return storage_service.create(db, obj_in=obj_in)

# 3. Get by ID (GET /{id})
@router.get("/{id}", response_model=StorageResponse)
def read_device(id: UUID, db: Session = Depends(get_db)):
    device = storage_service.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# 4. Full update (PUT /{id})
@router.put("/{id}", response_model=StorageResponse)
def update_device_full(id: UUID, obj_in: StorageCreate, db: Session = Depends(get_db)):
    device = storage_service.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return storage_service.update(db, db_obj=device, obj_in=StorageUpdate(**obj_in.model_dump()))

# 5. Partial update (PATCH /{id})
@router.patch("/{id}", response_model=StorageResponse)
def update_device_partial(id: UUID, obj_in: StorageUpdate, db: Session = Depends(get_db)):
    device = storage_service.get(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return storage_service.update(db, db_obj=device, obj_in=obj_in)

# 6. Soft delete (DELETE /{id})
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(id: UUID, db: Session = Depends(get_db)):
    device = storage_service.remove(db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return None