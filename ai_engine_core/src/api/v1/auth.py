import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

from src.db.session import get_db
from src.db.models import UserModel

router = APIRouter(prefix="/auth", tags=["Authentication & Scurity"])

# cấu hình mã hóa mật khẩu và jwt token
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "khoa-bi-mat-sieu-cap-doanh-nghiep-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*4
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# 1. schemas pydantic
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str="người dùng mới"
    
class TokenResponse(BaseModel):
    acccess_token: str
    token_type: str = "bearer"
    
# 2. các hàm tiện ích bảo mật 
def hash_password(password: str) -> str:
    """mã hóa mật khẩu 1 chiều bằng Bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) ->bool:
    """kiểm tra mật khẩu đầu vào có đúng không"""
    return pwd_context.verify(plain_password, hash_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None) -> str:
    """tạo ra chuỗi thẻ bài jwt token có hạn sử dụng"""
    to_encode= data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 3. hàm kiểm tra thẻ bài 
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession=Depends(get_db)) -> UserModel:
    """kiểm tra xem user có giơ đúng thẻ bài jwt hợp lệ không"""
    auth_error = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="thẻ bài jwt không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise auth_error
        
    except jwt.PyJWKError:
        raise auth_error
    
    user = await db.get(UserModel, user_id)
    if user is None:
        raise auth_error
    return user

# 4. endpoint: đăng ký và đăng nhập
@router.post("/register", summary="đăng ký tài khoản mới")
async def register(req: UserRegisterRequest, db: AsyncSession=Depends(get_db)):
    """tạo tài khoản mới, mật khẩu sẽ được băm tự động"""
    # kiểm tra email đã tồn tại chưa
    stmt = select(UserModel).where(UserModel.email == req.email)
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="email này đã được đăng ký mới")
    
    # tạo user với mật khẩu đã mở khóa
    new_user = UserModel(
        email = req.email,
        full_name = req.full_name,
        hashed_password = hash_password(req.password)
    )
    db.add(new_user)
    await db.commit()
    return {"status": "success", "message": f"đăng ký thành công cho {req.email}!"}

@router.post("/login", response_model= TokenResponse, summary="đăng nhập lấy jwt token")
async def login(form_data: OAuth2PasswordRequestForm= Depends(), db: AsyncSession=Depends(get_db)):
    """đăng nhập bằng email và password để lấy thẻ bài jwt"""
    stmt = select(UserModel).where(UserModel.email == form_data.username)
    user = (await db.excute(stmt).scalar_one_or_none())
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "sai email hoặc mật khẩu"
        )
    
    # sinh thẻ bài jwt token có thời hạn 24h
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return TokenResponse(access_token = access_token)