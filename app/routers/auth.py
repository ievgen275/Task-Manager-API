from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from sсhemas.schemas import UserLoginSchema
from dependencies import SessionDep
from core.config import config
from authx import AuthX
from sqlalchemy import select
from models.models import UserModel

router = APIRouter(tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = AuthX(config=config)

@router.post("/login")
async def login(creds: UserLoginSchema, session: SessionDep):
    result = await session.execute(select(UserModel).where(UserModel.username == creds.username))
    user = result.scalar()

    if not user or not pwd_context.verify(creds.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = security.create_access_token(uid=str(user.id))
    refresh_token = security.create_refresh_token(uid=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }