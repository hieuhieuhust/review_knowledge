from datetime import datetime
from sqlalchemy import Integer, String, text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.session import Base

# --- bảng usermodel (tài khoảng người dùng)
class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True,index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True,index=True,nullable=False)
    full_name: Mapped[str] =mapped_column(String(100), default="người dùng mới")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # 1 user sở hữu nhiều  cuộc nói chuyện
    conversations: Mapped[list["ConversationModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
class ConversationModel(Base):
    __tablename__ = "conversation"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True,index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True,nullable=True)
    title: Mapped[str] = mapped_column(String(255), default="cuộc trò chuyện mới")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    user:Mapped["UserModel"] = relationship(back_populates="conversations")
    messages: Mapped[list["MessageModel"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan"
    )
    
# bảng messagemodel (tin nhắn qua chat)
class MessageModel(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True,index=True)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversation.id"), index=True)
    role: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(text)
    created_at: Mapped[datetime] = mapped_column(datetime, default=datetime.utcnow)
    
    conversation: Mapped["ConversationModel"] = relationship(back_populates="messages")