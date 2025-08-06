from fastapi import APIRouter

from .notifications import router as notifications_router

router = APIRouter()

router.include_router(notifications_router, tags=['dashboard_notifications'])
