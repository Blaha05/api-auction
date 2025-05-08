from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from services.ORMservice import service_factory
from config.db.db_helper import async_session
from models.auction import Auction
from models.history import History
from models.user import User
from models.messege import Folow
from services.wsservice import ConnectionManager
from services.suthservice import AuthService
from config.user_congig import token
from tasks.sendemail import sendemail, check_email

router = APIRouter(
    tags=['history']
)

manager = ConnectionManager()

service_auth_token = token
service_auth = AuthService(User)
service_history = service_factory(async_session, History)
service_auction = service_factory(async_session, Auction)
service_user = service_factory(async_session, User)
service_follow = service_factory(async_session, Folow)

@router.websocket("/bit")
async def websocket_endpoint(websocket: WebSocket, id:int, token):
        await manager.connect(websocket)
        user = service_auth_token.decode_token(token)

        auction = await service_auction.get_one({'id':id})
        try:
            while True:
                data = await websocket.receive_text()
                user_db = await service_user.get_one({'id':user['id']})

                if user_db[0].balance < int(data):
                    await websocket.send_text("You do not have enough money")
                    continue
                    
                if int(data) - auction[0].curr_price >= auction[0].step_bit:

                    bit = await service_history.create({
                        'id_user':user['id'],
                        'id_auction':auction[0].id,
                        'bit':int(data)
                    })

                    await service_auction.update({'curr_price':int(data)}, {'id':id})

                    user_follow = await service_follow.get_one({'id_auction':auction[0].id})
                    check_email.apply_async(args=[user_follow, user['id']])

                    await manager.broadcast(f"Bit now: {auction[0].curr_price}") 
                else:
                    await websocket.send_text("Your bit is less than the step bit")             
        except WebSocketDisconnect:
            manager.disconnect(websocket)


@router.get('/get_history')
async def get_history(id:int):
    return await service_history.get_one({'id_auction':id}) 

@router.post('/follow_auction')
async def follow_auction(id:int, user = Depends(service_auth.get_current_user)):
    return await service_follow.create({'email':user['email'], 'id_auction':id})

@router.delete('/unfollow_auction')
async def unfollow_auction(id:int, user = Depends(service_auth.get_current_user)):
    return await service_follow.delete({'id_auction':id, 'email':user['email']})

@router.get('/task_celery1')
async def get_follow():
    #sendemail.delay(f"Your bit", 'blaha.viktor@student.uzhnu.edu.ua')
    sendemail.apply_async(args=["test message", "blaha.viktor@student.uzhnu.edu.ua"])
    return {'data':'ok'}

@router.get('/task_celery2')
async def get_follow():
    user_follow = await service_follow.get_one({'id_auction':4})
    emails = [i.email for i in user_follow]
    check_email.apply_async(args=[emails, 2])
    return {'data':'ok'}