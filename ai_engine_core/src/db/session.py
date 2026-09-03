import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

# 1. đọc file .env để lấy mật khẩu thông tin kết nối
load_dotenv()

# 2. lấy linh kết nối postgresql từ file .env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_chat_db"
)

# 3. tạo cỗ máy kết nối bất đồng bộ (async engine) với postgresql
engine = create_async_engine(DATABASE_URL, echo =False)

# 4. nhà máy sinh ra các phiên làm việc (session) với database
AsyncSesssionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

# 5. lớp base cha cho các bảng trong models.py
class Base(DeclarativeBase):
    pass

# 6. hàm get_db (chính là hàm auth.py đang tìm):
# mỗi khi có request gọi api, hàm này sẽ mở 1 kết nối và  tự động đóng khi xong việc
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSesssionLocal() as session:
        yield session