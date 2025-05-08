from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from config.db.db_helper import Base

class Massege(Base):
    __tablename__ = "messege"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    auction_name: Mapped[str] = mapped_column(String(320), nullable=False)
    time:Mapped[DateTime] = mapped_column(DateTime)


class Folow(Base):
    __tablename__ = "follow"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    id_auction: Mapped[int] = mapped_column(nullable=False)