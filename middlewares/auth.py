from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from connections import get_session
from repository import TokenRepository
from utils import token_validator
from http import HTTPStatus
from typing import Annotated


oauth_schema = OAuth2PasswordBearer(tokenUrl="token")


async def auth_user(request: Request, session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        token = (
            request.headers["Authorization"]
            .removeprefix("bearer ")
            .removeprefix("Bearer ")
        )
        if not await TokenRepository(session).revoke_token(token):
            return token_validator(token)
        else:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)
    except KeyError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED)
