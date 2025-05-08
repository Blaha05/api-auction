from pydantic import BaseModel, EmailStr

class AddUserShema(BaseModel):
    email:EmailStr
    name:str
    password:str

class UpdateUserShema(BaseModel):
    email:EmailStr | None = None
    name:str | None = None
    password:str | None = None

class FillterUserShema(BaseModel):
    email:EmailStr | None = None
    name:str | None = None
    id:int | None = None

    def add_id(self, id):
        self.id = id
        return self


