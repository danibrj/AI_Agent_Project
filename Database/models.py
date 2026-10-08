from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Conversation(Base):
    __tablename__ = "Conversation History"
    
    id = Column(Integer,primary_key=True)
    created_at = Column(String)
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "Message"
    
    id = Column(Integer,primary_key=True)
    conversation_id = Column(
        Integer,
        ForeignKey("Conversation History.id")
)
    role = Column(String)
    content = Column(String)
    created_at = Column(String)
    conversation = relationship("Conversation", back_populates="message")
    
    
    