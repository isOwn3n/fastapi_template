from middlewares import auth_user
from schema import LoginInfo, Token

from connections import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.routing import APIRouter
from typing import Annotated
from fastapi import Depends, Header
from repository import UserRepository
from schema import JWTData
from utils import token_generate


auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(
    user_info: LoginInfo,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    repo = UserRepository(session)
    u = await repo.check_password(user_info.username, user_info.password)
    ur = await repo.get_user_roles(u.id)
    data = JWTData(roles=ur, user_id=str(u.id))
    token = token_generate(data)
    return Token(access_token=token)

@auth_router.post("/logout")
async def logout(
    _: Annotated[JWTData, Depends(auth_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    authorization: str = Header(None)
):
    # Retrieve the token from the Authorization header
    token = authorization.split("Bearer ")[1]
    repo = UserRepository(session)
    return await repo.logout(token)


@auth_router.get("/token")
async def token(user_info: Annotated[JWTData, Depends(auth_user)]):
    return user_info
