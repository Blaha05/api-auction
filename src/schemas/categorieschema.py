from pydantic import BaseModel
from typing import Optional

class AddCoategorieSchema(BaseModel):
    id_auction: int
    categorie: str


class FillteroategorieSchema(BaseModel):
    id:Optional[int] = None
    id_auction:Optional[int] = None
    categorie:Optional[str] = None

class UpdateoategorieSchema(BaseModel):
    categorie: Optional[str] = None
