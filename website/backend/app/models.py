from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Novel(Base):
    __tablename__ = "novels"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    image_url = Column(String, nullable=True)
    
    # Relationship to chapters
    chapters = relationship("Chapter", back_populates="novel", order_by="Chapter.number")

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    number = Column(Integer)
    content = Column(String)
    novel_id = Column(Integer, ForeignKey("novels.id"))
    
    # Relationship to novel
    novel = relationship("Novel", back_populates="chapters")