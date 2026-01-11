from .document import document_router

from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(document_router)

__all__ = ("v1_router",)