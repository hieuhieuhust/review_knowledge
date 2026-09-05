import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr

from src.db.session import get_db
from src.db.models import UserModel

router = APIRouter(prefix="/auth", tags=["Authentication & Security"])

SECRET_KEY = "khoa-bi-mat-sieu-cap-doanh-nghiep-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# --- 1. SCHEMAS PYDANTIC ---
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str = "Người dùng mới"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- 2. HÀM MÃ HÓA BCRYPT GỐC ---
def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- 3. DEPENDENCY KIỂM TRA USER ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UserModel:
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise auth_error
    except jwt.PyJWTError:
        raise auth_error

    user = await db.get(UserModel, user_id)
    if user is None:
        raise auth_error
    return user


# --- 4. ENDPOINTS REGISTER & LOGIN ---
@router.post("/register", summary="Đăng ký tài khoản mới")
async def register(req: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    # 1. Kiểm tra email đã có chưa
    stmt = select(UserModel).where(UserModel.email == req.email)
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email này đã được đăng ký!")

    # 2. Tạo User và băm mật khẩu
    new_user = UserModel(
        email=req.email,
        full_name=req.full_name,
        hashed_password=hash_password(req.password)
    )
    db.add(new_user)
    await db.commit()
    return {"status": "success", "message": f"Đăng ký thành công cho {req.email}!"}


@router.post("/login", response_model=TokenResponse, summary="Đăng nhập lấy JWT Token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    stmt = select(UserModel).where(UserModel.email == form_data.username)
    user = (await db.execute(stmt)).scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai email hoặc mật khẩu!"
        )

    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return TokenResponse(access_token=access_token)