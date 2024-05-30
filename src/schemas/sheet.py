import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Sequence
from sqlalchemy.orm import relationship, Mapped

from database import Base


class Sheet(Base):
    __tablename__ = "sheets"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="sheets")
    name = Column(String(255))
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.now)
    modified_at: Mapped[datetime.datetime] = Column(DateTime, onupdate=datetime.datetime.now)