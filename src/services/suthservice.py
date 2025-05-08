from fastapi import Depends, HTTPException, Request, status
from schemas.user import AddUserShema
from services.ORMservice import service_factory
from config.db.db_helper import async_session
from config.user_congig import services_users
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthService:
    def __init__(self, model):
        self.model = model
        self.user_service = service_factory(async_session, self.model)
        services = services_users()
        self.token = services['token']
        self.hashed_password = services['hashed_password']


    async def register(self, data:AddUserShema) -> str:
        data.password = self.hashed_password.hashed_password(data.password).decode()
        try:
            user = await self.user_service.create(data)
            data_for_token = {
                    'id': user.id,
                    'email': user.email,
                    'username': user.name,
                    'is_admin': user.is_admin
                }
            return self.token.create_token(data_for_token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: this email is already registered. {str(e)}"
            )
        

    async def login(self, data:OAuth2PasswordRequestForm = Depends()) -> str:
        user = await self.user_service.get_one({'email':data.username})
        user = user[0]
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: this email is not registered."
            )
        if not self.hashed_password.check_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: password is not correct."
            )
        data_for_token = {
            'id': user.id,
            'email': user.email,
            'username': user.name,
            'is_admin': user.is_admin
        }
        return self.token.create_token(data_for_token)
    

    async def get_current_user(self,
        token: str = Depends(oauth2_scheme),
    ):
        return self.token.decode_token(token)
    
    async def get_access(self, request: Request):
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        scheme, _, param = authorization.partition(" ")
        user = self.token.decode_token(param)
        return user['is_admin']


