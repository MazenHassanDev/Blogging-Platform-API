from sqlalchemy import String, Integer, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database import Base

class Post(Base):
    __tablename__ = 'posts'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String(255), nullable=False)
    content:Mapped[str] = mapped_column(Text, nullable=False)
    category:Mapped[str] = mapped_column(String(100), nullable=False)
    tags:Mapped[str] = mapped_column(JSON, nullable=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
