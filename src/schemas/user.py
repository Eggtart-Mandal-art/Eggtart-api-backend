from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.types import Enum

from database import Base
from enums import SocialProvider
from schemas import Sheet


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    nickname = Column(String(255))
    social_id = Column(String(255))
    social_provider = Column(Enum(SocialProvider, native_enum=False))
    sheets: Mapped[Sheet] = relationship("Sheet", back_populates="owner")
    apple_refresh_token = Column(String(255), nullable=True)
