from fastapi import APIRouter
from .v1 import document_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(document_router)

__all__ = ("v1_router",)