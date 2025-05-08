from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from services.ORMservice import service_factory
from config.db.db_helper import async_session
from models.auction import Auction, Foto, Categorie
from schemas.auctionschema import AddAuctionSchema, FillterAuctionSchema, UpdateAuctionSchema
from services.suthservice import AuthService
from models.user import User
from config.aws_config import s3
from fastapi_cache.decorator import cache


service_user = AuthService(User)

service = service_factory(async_session, Auction)
service_foto = service_factory(async_session, Foto)
service_categorie = service_factory(async_session, Categorie)

router = APIRouter(
    tags=['auction']
)

@router.get('/get_auction')
@cache(expire=60)
async def get_auction():
    return await service.get_all()

@router.post('/add_auction')
async def create_auction(data: AddAuctionSchema, user = Depends(service_user.get_current_user)):
    data = data.model_copy(update={"id_user": user['id']}) 
    return await service.create(data)

@router.put('/change_auction')
async def update_auction(data: UpdateAuctionSchema, filter: FillterAuctionSchema, user = Depends(service_user.get_current_user)):
    cur_auction = await service.get_one(filter)
    if cur_auction[0].id_user != user['id']:
        raise HTTPException(status_code=403, detail="You are not the author of the auction")
    action  = await service.update(data, filter)
    return {'data' : 'update'}

@router.get('/get_filter_auction')
@cache(expire=60)
async def get_one_auction(data: FillterAuctionSchema = Depends()):
    id_auctions = []
    to, data.to = data.to, None
    if data.categorie:
        auctions = await service_categorie.get_one({'categorie':data.categorie})
        for auction in auctions:
            id_auctions.append(auction.id_auction)
        data.categorie = None
        auc = await service.get_one(data)
        res = [auction for auction in auc if auction.id in id_auctions]
        if to:
            res = [auction for auction in res if auction.finish_at <= to]
        return res
    res =  await service.get_one(data)
    if to:
        res = [auction for auction in res if auction.finish_at <= to]
    return res


@router.delete('/delete_auction')
async def delete_auction(data: FillterAuctionSchema, user = Depends(service_user.get_current_user)):
    cur_auction = await service.get_one(data)
    if cur_auction[0].id_user == user['id'] or user['is_admin']:
        return await service.delete(data)
    raise HTTPException(status_code=403, detail="You are not the author of the auction")

@router.post("/upload-to-bucket/")
async def upload_to_bucket(id_auction:int, file: UploadFile = File(...)):
    s3.upload_fileobj(
        file.file,  
        'auctionblaha',  
        file.filename,  
        ExtraArgs={"ACL": "public-read"}
    )
    photo = await service_foto.create({'id_auction':id_auction,'path':f'https://auctionblaha.s3.us-east-1.amazonaws.com/{file.filename}'})

    return photo

@router.get('/get_photo')
@cache(expire=60)
async def get_fillter_foto(id_auction:int):
    return await service_foto.get_one({'id_auction':id_auction})

@router.delete('/delete_photo')
async def delete_photo(data: FillterAuctionSchema):
    return await service_foto.delete(data)