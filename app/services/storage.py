from sqlalchemy.orm import Session
from sqlalchemy import func, select
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Tuple

from app.models.storage import StorageDevice
from app.schemas.storage import StorageCreate, StorageUpdate

class StorageService:
    # 1. Получение списка с пагинацией и учетом Soft Delete
    def get_multi(
        self, db: Session, *, page: int = 1, limit: int = 10
    ) -> Tuple[List[StorageDevice], int]:
        # Рассчитываем смещение (offset) для SQL-запроса
        offset = (page - 1) * limit
        
        # Запрос: выбираем только те записи, где deleted_at IS NULL
        base_query = select(StorageDevice).where(StorageDevice.deleted_at == None)
        
        # Считаем общее количество активных записей для мета-данных пагинации
        total_count = db.scalar(
            select(func.count()).select_from(base_query.subquery())
        )
        
        # Получаем данные конкретной страницы
        items = db.execute(
            base_query.offset(offset).limit(limit)
        ).scalars().all()
        
        return items, total_count

    # 2. Получение одного активного устройства по ID
    def get(self, db: Session, id: UUID) -> Optional[StorageDevice]:
        # Убеждаемся, что мы не возвращаем "soft delete" записи
        return db.query(StorageDevice).filter(
            StorageDevice.id == id, 
            StorageDevice.deleted_at == None
        ).first()

    # 3. Создание новой записи 
    def create(self, db: Session, *, obj_in: StorageCreate) -> StorageDevice:
        db_obj = StorageDevice(
            model=obj_in.model,
            serial_number=obj_in.serial_number,
            capacity_gb=obj_in.capacity_gb,
            status=obj_in.status
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # 4. Частичное обновление (PATCH)
    def update(self, db: Session, *, db_obj: StorageDevice, obj_in: StorageUpdate) -> StorageDevice:
        # Превращаем DTO в словарь, исключая неуказанные поля
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # 5. Реализация Мягкого удаления (Soft Delete)
    def remove(self, db: Session, *, id: UUID) -> Optional[StorageDevice]:
        db_obj = self.get(db, id)
        if db_obj:
            db_obj.deleted_at = datetime.now()
            db.add(db_obj)
            db.commit()
        return db_obj

# Экземпляр для импорта в контроллеры
storage_service = StorageService()