"""
Authentication Routes - Better Auth Integration
Task: T022 [US1] Authentication routes per plan.md
"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, field_validator
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.database import get_db
from jose import jwt
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
import uuid
import os

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# JWT Configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


class SignupRequest(BaseModel):
    """Request model for user signup"""
    email: EmailStr
    password: str
    name: str

    @field_validator('password')
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class LoginRequest(BaseModel):
    """Request model for user login"""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Response model for authentication"""
    token: str
    user: dict


def hash_password(password: str) -> str:
    """Hash a password using SHA256 with salt (simpler, no bcrypt issues)"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${password_hash}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verify a password against its hash"""
    try:
        salt, password_hash = stored_hash.split('$')
        return hashlib.sha256((plain_password + salt).encode()).hexdigest() == password_hash
    except ValueError:
        return False


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    """
    User registration endpoint.
    Creates a new user account and returns JWT token.
    """
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == request.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = hash_password(request.password)

    new_user = User(
        id=str(uuid.uuid4()),
        email=request.email,
        name=request.name,
        password_hash=hashed_password,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": new_user.id,
            "email": new_user.email,
            "name": new_user.name
        }
    )

    return AuthResponse(
        token=access_token,
        user={
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name
        }
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    User login endpoint.
    Authenticates user and returns JWT token.
    """
    # Find user by email
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
            "name": user.name
        }
    )

    return AuthResponse(
        token=access_token,
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    """
    User logout endpoint.
    JWT tokens are stateless, logout is handled client-side.
    """
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user(db: AsyncSession = Depends(get_db)):
    """Get current user info - placeholder for token verification"""
    return {"message": "Use token to get user info"}
