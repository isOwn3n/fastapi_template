from http import HTTPStatus
from models.token import RevokeToken

from schema import UserGetResponse
from utils import token_exp_date, token_validator

from .base import BaseRepository
from fastapi import HTTPException

from models import (
    User,
    User_Role,
    Role,
    Resource,
    Resource_Role,
)
from sqlmodel import select
from utils import generate_password, check_password as password_check
from datetime import datetime
from sqlalchemy.exc import NoResultFound


class UserRepository(BaseRepository):
    async def list(self, limit, offset) -> UserGetResponse:
        try:
            s = select(User).where(User.deleted_at == None).limit(limit).offset(offset)
            return (await self.session.exec(s)).all()
        except NoResultFound:
            raise HTTPException(HTTPStatus.NOT_FOUND)

    async def create(self, user: User):
        try:
            s = User(
                username=user.username,
                email=user.email,
                password=generate_password(user.password).decode(),
            )

            self.session.add(s)
            await self.session.commit()
            await self.session.refresh(s)
            await self.session.close()
            return await self.get(s.id)
        except NoResultFound:
            raise HTTPException(HTTPStatus.FORBIDDEN)
        except:
            raise HTTPException(HTTPStatus.BAD_REQUEST)

    async def get(self, uid):
        s = select(User).where(User.id == uid).where(User.deleted_at == None)
        return (await self.session.exec(s)).first()

    async def update(self, uid, user: User):
        try:
            s = select(User).where(User.id == uid).where(User.deleted_at == None)
            user_db = (await self.session.exec(s)).first()

            user_db.username = user.username
            user_db.email = user.email
            user_db.updated_at = datetime.now().replace(tzinfo=None)

            self.session.add(user_db)
            await self.session.commit()
            await self.session.refresh(user_db)
            return await self.get(uid)

        except NoResultFound:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        except:
            raise HTTPException(HTTPStatus.BAD_REQUEST)

    async def delete(self, uid):
        try:
            s = (
                await self.session.exec(
                    select(User).where(User.id == uid).where(User.deleted_at == None)
                )
            ).one()
            s.deleted_at = datetime.now().replace(tzinfo=None)

            self.session.add(s)
            await self.session.commit()
            await self.session.refresh(s)
            await self.session.close()
            return await self.get(s.id)
        except NoResultFound:
            raise HTTPException(HTTPStatus.NOT_FOUND, "User Is Not Available!")

    async def check_password(self, username: str, password: str):
        try:
            s = (
                select(User)
                .where(User.username == username)
                .where(User.deleted_at == None)
            )
            result = (await self.session.exec(s)).one()

            if password_check(password, result.password):
                return result
            else:
                raise HTTPException(HTTPStatus.FORBIDDEN, "Wrong Username or Password!")
        except NoResultFound:
            raise HTTPException(HTTPStatus.FORBIDDEN, "Wrong Username or Password!")

    async def change_password(self, uid: int, password: str, new_password: str):
        try:
            if password == new_password:
                raise HTTPException(
                    HTTPStatus.BAD_REQUEST,
                    "New Password Can Not Be The Same As Old One!",
                )
            s = select(User).where(User.id == uid).where(User.deleted_at == None)
            user_db = (await self.session.exec(s)).one()
            if password_check(password, user_db.password):
                user_db.password = generate_password(new_password).decode()
                user_db.updated_at = datetime.now().replace(tzinfo=None)

                self.session.add(user_db)
                await self.session.commit()
                await self.session.refresh(user_db)
                return {"message": "Password Changed Successfully!"}
            else:
                raise HTTPException(HTTPStatus.FORBIDDEN, "Wrong Password!")
        except NoResultFound:
            raise HTTPException(HTTPStatus.NOT_FOUND)

    async def get_user_roles(self, uid):
        try:
            s = (
                select(Role.roleName)
                .where(User.id == uid)
                .where(User_Role.role_id == Role.id)
                .where(User_Role.user_id == User.id)
                .join(User_Role, User_Role.role_id == Role.id)
                .join(User, User_Role.user_id == User.id)
            )
            return (await self.session.exec(s)).all()
        except NoResultFound:
            raise HTTPException(HTTPStatus.FORBIDDEN, "Permission Denied!")

    async def get_rol_resources(self, role):
        try:
            s = (
                select(Resource.resourceName, Resource_Role)
                .where(Resource_Role.resource_id == Resource.id)
                .where(Resource_Role.role_id == Role.id)
                .where(Role.name == role)
                .join(Resource_Role, Resource_Role.role_id == Role.id)
                .join(Resource, Resource_Role.resource_id == Resource.id)
            )

            return (await self.session.exec(s)).all()
        except NoResultFound:
            raise Exception(HTTPStatus.FORBIDDEN, "Permission Denied!")

    async def logout(self, token):
        try:
            if (await self.session.exec(select(RevokeToken).where(RevokeToken.token == token))).one():
                raise HTTPException(HTTPStatus.UNAUTHORIZED)
        except NoResultFound:
            token_exp = datetime.fromtimestamp(token_exp_date(token))
            s = RevokeToken(
                user_id=token_validator(token).user_id,
                token=token,
                rev_date=token_exp,
                logged_out=True,
            )

            self.session.add(s)
            await self.session.commit()
            await self.session.refresh(s)
            await self.session.close()
            return {"message": "Logged out successfully"}
