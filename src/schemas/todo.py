import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Sequence
from sqlalchemy.orm import relationship, Mapped

from database import Base


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    cell_id = Column(Integer, ForeignKey("cells.id"))
    cell = relationship("Cell")
    content = Column(String(255))
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.now)
    modified_at: Mapped[datetime.datetime] = Column(DateTime, onupdate=datetime.datetime.now)