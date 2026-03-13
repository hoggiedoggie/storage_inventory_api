from fastapi import APIRouter
from app.api.v1.endpoints import storage

api_router = APIRouter()
api_router.include_router(storage.router, prefix="/devices", tags=["storage"])