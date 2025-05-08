from pydantic import BaseModel
from typing import Optional

class AddCommentSchema(BaseModel):
    id_auction: int
    coment: str
    id_user: int = 1

class FillterCommentSchema(BaseModel):
    id:Optional[int] = None
    id_auction:Optional[int] = None
    id_user:Optional[int] = None
    coment:Optional[str] = None

class UpdateCommentSchema(BaseModel):
    coment: Optional[str] = None
