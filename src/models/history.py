from config.db.db_helper import Base
from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class History(Base):
    __tablename__ = 'user_bits'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    id_auction:Mapped[int] = mapped_column(ForeignKey('auctions.id', ondelete='CASCADE'))
    id_user:Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    bit:Mapped[Numeric] = mapped_column(Numeric, nullable=False)