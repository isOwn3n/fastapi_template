from http import HTTPStatus
from middlewares import auth_user
from schema import (
    JWTData,
    UserGetResponse,
    UserCreateRequest,
    UserUpdateRequest,
    UserChangePasswordRequest,
)
from utils import has_access, ResourceValue

from repository import UserRepository
from connections import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.routing import APIRouter
from typing import Annotated, List
from fastapi import HTTPException, Query, Depends


user_router = APIRouter()


@user_router.get("/", response_model=List[UserGetResponse])
async def read_user(
    user_info: Annotated[JWTData, Depends(auth_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = Query(default=10, le=100),
):
    roles = user_info.roles
    repo = UserRepository(session)
    access = await has_access(roles, "user", ResourceValue.VIEW, repo)
    if access:
        return await repo.list(limit, offset)
    else:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Access Denied!")


@user_router.post("/", response_model=UserGetResponse)
async def create_user(
    user_info: Annotated[JWTData, Depends(auth_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    user: UserCreateRequest,
):
    roles = user_info.roles
    repo = UserRepository(session)
    access = await has_access(roles, "user", ResourceValue.ADD, repo)
    if access:
        return await repo.create(user)
    else:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Access Denied!")


@user_router.put("/{uid}", response_model=UserGetResponse)
async def update_user(
    user_info: Annotated[JWTData, Depends(auth_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    uid: int,
    user: UserUpdateRequest,
):
    roles = user_info.roles
    repo = UserRepository(session)
    access = await has_access(roles, "user", ResourceValue.EDIT, repo)
    if access:
        return await repo.update(uid, user)
    else:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Access Denied!")


@user_router.put("/delete/{uid}/")
async def delete_user(
    user_info: Annotated[JWTData, Depends(auth_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    uid: int,
):
    roles = user_info.roles
    repo = UserRepository(session)
    access = await has_access(roles, "user", ResourceValue.DELETE, repo)
    if access:
        return await repo.delete(uid)
    else:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Access Denied!")


@user_router.put("/change-password/")
async def change_password(
    user_info: Annotated[JWTData, Depends(auth_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    user: UserChangePasswordRequest,
):
    repo = UserRepository(session)
    return await repo.change_password(int(user_info.user_id), user.password, user.new_password)
