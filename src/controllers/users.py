from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from config.db.db_helper import async_session
from models.user import User
from services.ORMservice import ORMService
from services.suthservice import AuthService
from schemas.user import AddUserShema, UpdateUserShema, FillterUserShema
from fastapi_cache.decorator import cache


router = APIRouter(
    tags=['users']
)

service = ORMService(async_session, User)
service_user = AuthService(User)

@router.get("/users/")
@cache(expire=60)
async def get_users():
    return await service.get_all()

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return await service.get_one({'id':user_id})

@router.post("/register")
async def add_user(user: AddUserShema):
    return await service_user.register(user)

@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    return await service_user.login(data)

@router.put("/update_user")
async def update_user(user: UpdateUserShema, user_curr = Depends(service_user.get_current_user)):
    await service.update(user, {'id': user_curr['id']})
    return {'data': 'update'}

@router.delete("/delete_user")
async def delete_user(user = Depends(service_user.get_current_user)):
    await service.delete({'id': user['id']})
    return {'data': 'delete'}

