from fastapi import APIRouter
from controllers.users import router as user_router
from controllers.auction import router as auction_router
from controllers.comment import router as comment_router
from controllers.categorie import router as categorie_router
from controllers.history import router as history_router

router = APIRouter()

router.include_router(user_router)
router.include_router(auction_router)
router.include_router(comment_router)
router.include_router(categorie_router)
router.include_router(history_router)
