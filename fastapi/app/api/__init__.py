from fastapi import APIRouter


from .user import router as users_router
from .auth import router as auth_router
from .city import router as city_router

router = APIRouter()

router.include_router(users_router)
router.include_router(auth_router)
router.include_router(city_router)