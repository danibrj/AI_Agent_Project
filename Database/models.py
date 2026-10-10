from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Database.database import Base

class Conversation(Base):
    __tablename__ = "Conversations"
    
    id = Column(Integer,primary_key=True)
    created_at = Column(String)
    test_key = Column(String, unique=True, nullable=True)
    messages = relationship("Message", back_populates="conversation")
    


class Message(Base):
    __tablename__ = "Message"
    
    id = Column(Integer,primary_key=True)
    conversation_id = Column(
        Integer,
        ForeignKey("Conversations.id")
    )
    role = Column(String)
    content = Column(String)
    created_at = Column(String)
    conversation = relationship("Conversation", back_populates="messages")
    
    
    