from typing import Annotated
from fastapi import Depends
from database import new_session
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]