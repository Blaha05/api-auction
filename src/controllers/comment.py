from fastapi import APIRouter, Depends, HTTPException
from models.auction import Coment  
from models.user import User
from services.ORMservice import service_factory
from config.db.db_helper import async_session
from schemas.commentschema import AddCommentSchema, FillterCommentSchema, UpdateCommentSchema
from services.suthservice import AuthService
from fastapi_cache.decorator import cache


service = service_factory(async_session, Coment)
service_user = AuthService(User)


router = APIRouter(
    tags=['comment']
)


@router.get("/comments/")
@cache(expire=60)
async def get_comments():
    return await service.get_all()

@router.post("/add_comment")
async def add_comment(data: AddCommentSchema, user = Depends(service_user.get_current_user)):
    data = data.model_copy(update={"id_user": user['id']})
    return await service.create(data)

@router.get("/get_one_comment")
@cache(expire=60)
async def get_one_comment(data: FillterCommentSchema = Depends()):
    return await service.get_one(data)

@router.put("/update_comment")
async def update_comment(
        data: UpdateCommentSchema, 
        fillter: FillterCommentSchema,
        user: dict = Depends(service_user.get_current_user)
    ):
    cur_coment = await service.get_one(fillter)
    if cur_coment[0].id_user != user['id']:
        raise HTTPException(status_code=403, detail="You are not the author of the auction")
    await service.update(data, fillter)
    return {'data' : 'update'}

@router.delete("/delete_comment")
async def delete_comment(data: FillterCommentSchema, user = Depends(service_user.get_current_user)):
    cur_coment = await service.get_one(data)
    if cur_coment[0].id_user == user['id'] or user['is_admin']:
        return await service.delete(data)
    raise HTTPException(status_code=403, detail="You are not the author of the auction")

