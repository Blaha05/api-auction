from fastapi import APIRouter, Depends
from models.auction import Categorie  
from models.user import User
from services.ORMservice import service_factory
from config.db.db_helper import async_session
from schemas.categorieschema import AddCoategorieSchema, FillteroategorieSchema
from services.suthservice import AuthService
from fastapi_cache.decorator import cache


service = service_factory(async_session, Categorie)
service_user = AuthService(User)

router = APIRouter(
    tags=['categorie']
)

@router.get("/categories")
@cache(expire=60)
async def get_comments():
    return await service.get_all()

@router.post("/add_categorie")
async def add_categorie(data: AddCoategorieSchema, user = Depends(service_user.get_current_user)):
    data = data.model_copy(update={"id_user": user['id']})
    return await service.create(data)

@router.get("/get_one_categories")
@cache(expire=60)
async def get_one_categorie(data: FillteroategorieSchema = Depends()):
    return await service.get_one(data)

@router.delete("/delete_categorie")
async def delete_categorie(data: FillteroategorieSchema, user = Depends(service_user.get_current_user)):
    data = data.model_copy(update={"id_user": user['id']})
    return await service.delete(data)


