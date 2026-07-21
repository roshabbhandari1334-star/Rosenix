import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr

from backend.database.postgres import get_db_session
from backend.database.models.user_model import UserModel, UserRole
from backend.api.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication & Security"])

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.OPERATOR

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db_session)):
    query = select(UserModel).where(
        (UserModel.username == user_in.username) | (UserModel.email == user_in.email)
    )
    existing_user = (await db.execute(query)).scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email already registered."
        )

    new_user = UserModel(
        id=str(uuid.uuid4()),
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role
    )
    db.add(new_user)
    await db.commit()
    return {"message": "User registered successfully", "id": new_user.id}

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    query = select(UserModel).where(UserModel.username == form_data.username)
    user = (await db.execute(query)).scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    return TokenResponse(access_token=access_token)