from fastapi import APIRouter


from .user import router as users_router
from .auth import router as auth_router
from .city import router as city_router
from .news import router as news_router
from .newstype import router as newstype_router

router = APIRouter()

router.include_router(users_router)
router.include_router(auth_router)
router.include_router(city_router)
router.include_router(newstype_router)
router.include_router(news_router)
