# Storage Inventory API

Профессиональная система учета накопителей (HDD/SSD) для инвентаризации серверного оборудования.

## Технологический стек
* **Backend:** Python 3.13 + FastAPI
* **Database:** PostgreSQL 16
* **ORM:** SQLAlchemy 2.0 + Alembic (миграции)
* **DevOps:** Docker & Docker Compose
* **Validation:** Pydantic v2 (схемы данных)

## Ключевые особенности
* **Soft Delete (Мягкое удаление):** Данные о дисках не удаляются физически, а помечаются как архивные (`deleted_at`). Это критично для сохранения истории серийных номеров.
* **UUID v4:** Использование защищенных уникальных идентификаторов вместо простых чисел.
* **Smart Pagination:** Список устройств возвращается с мета-данными (общее кол-во, текущая страница, лимит).
* **Docker-first:** Полная изоляция среды. Проект гарантированно запускается на Windows (через WSL2) и Linux.

##  Быстрый старт

### 1. Запуск инфраструктуры
```powershell
docker-compose up --build -d
```

### 2. Применение миграций
```
docker-compose exec app alembic revision --autogenerate -m "Initial"
docker-compose exec app alembic upgrade head
```

### 3. Документация
Интерфейс управления (Swagger) доступен по адресу:
 ```http://localhost:8000/docs```

### 4. Реализация Soft Delete
Команда, которая показывает "мягко" удаленные диски из таблицы
```docker-compose exec db psql -U postgres -d inventory_db -c "SELECT model, serial_number, deleted_at FROM storage_devices WHERE deleted_at IS NOT NULL;"```

### Примеры данных для тестирования (POST /api/v1/devices/)
Ниже приведены примеры реальных моделей накопителей для добавления в базу:
```
{
  "model": "Western Digital Red Plus 4TB",
  "serial_number": "WD-WCC7K4YV6L92",
  "capacity_gb": 4000,
  "status": "active"
}
{
  "model": "Seagate IronWolf 4TB",
  "serial_number": "ST4000VN008-2DR1",
  "capacity_gb": 4000,
  "status": "active"
}
{
  "model": "Western Digital Blue 1TB",
  "serial_number": "WD-WCC4N7XZL2K1",
  "capacity_gb": 1000,
  "status": "active"
}{
  "model": "HGST Ultrastar 7K6000",
  "serial_number": "HUA726020ALE610",
  "capacity_gb": 2000,
  "status": "active"
}
{
  "model": "Seagate Barracuda 2TB",
  "serial_number": "ST2000DM008-FAULTY",
  "capacity_gb": 2000,
  "status": "replacement_required"
}
```
