from fastapi import APIRouter

from .profiles import router as profiles_router
from .roles import router as roles_router
from .users import router as users_router

router = APIRouter()

router.include_router(users_router, tags=['users'])
router.include_router(profiles_router, tags=['profiles'])
router.include_router(roles_router, tags=['roles'])
