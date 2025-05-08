from sqlalchemy import Boolean, DateTime, Integer, String, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from config.db.db_helper import Base

class User(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    email:Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    name:Mapped[str] = mapped_column(String(320), nullable=False)
    password:Mapped[str] = mapped_column(String(1024), nullable=False)
    is_admin:Mapped[bool] = mapped_column(Boolean, default=False)
    created_at:Mapped[DateTime] = mapped_column(DateTime , server_default=func.now())
    balance:Mapped[Numeric] = mapped_column(Numeric, default=0.00)
