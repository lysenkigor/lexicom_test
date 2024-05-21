from fastapi import APIRouter

from src.api.v1.client_data import router as client_router

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(client_router)
