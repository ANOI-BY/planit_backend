from fastapi import Depends, FastAPI, HTTPException, APIRouter
from dependencies import get_token_header

from .users.methods import router as users_router
from .tables.methods import router as tables_router
from .columns.methods import router as columns_router
from .tasks.methods import router as tasks_router
from .auth.methods import router as auth_router

router = APIRouter(
    prefix="",
    # dependencies=[Depends(get_token_header)],
)

router.include_router(users_router)
router.include_router(tables_router)
router.include_router(columns_router)
router.include_router(tasks_router)
router.include_router(auth_router)
