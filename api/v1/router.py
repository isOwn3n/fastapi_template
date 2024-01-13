from fastapi.routing import APIRouter
from .user import user_router
from .auth import auth_router


router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(auth_router, prefix="/auth", tags=["auth", "user"])
