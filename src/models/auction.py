from config.db.db_helper import Base
from sqlalchemy import DateTime, Integer, Numeric, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Auction(Base):
    __tablename__ = 'auctions'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String(320), nullable=False)
    description:Mapped[str] = mapped_column(String(320), nullable=False)
    srart_price:Mapped[Numeric] = mapped_column(Numeric, default=0.00)
    curr_price:Mapped[Numeric] = mapped_column(Numeric, default=0.00)
    created_at:Mapped[DateTime] = mapped_column(DateTime , server_default=func.now())
    finish_at:Mapped[DateTime] = mapped_column(DateTime)
    id_user:Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    step_bit:Mapped[Numeric] = mapped_column(Numeric, default=0.00)


class Foto(Base):
    __tablename__ = 'fotos'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    id_auction:Mapped[int] = mapped_column(ForeignKey('auctions.id', ondelete='CASCADE'))
    path:Mapped[str] = mapped_column(String(320), nullable=False)


class Categorie(Base):
    __tablename__ = 'categories'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    id_auction:Mapped[int] = mapped_column(ForeignKey('auctions.id', ondelete='CASCADE'))
    categorie:Mapped[str] = mapped_column(String(320), nullable=False)


class Coment(Base):
    __tablename__ = 'coments'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    id_auction:Mapped[int] = mapped_column(ForeignKey('auctions.id', ondelete='CASCADE'))
    id_user:Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    coment:Mapped[str] = mapped_column(String(320), nullable=False)
