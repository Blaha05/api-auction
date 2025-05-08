from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class AddAuctionSchema(BaseModel):
    title: str
    description: str
    srart_price: Optional[Decimal] = 0.00
    curr_price: Optional[Decimal] = 0.00
    id_user: int = 1
    finish_at: datetime


class FillterAuctionSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    id_user: Optional[int] = None
    categorie: Optional[str] = None
    to:Optional[datetime] = None


class UpdateAuctionSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    finish_at: Optional[datetime] = None
