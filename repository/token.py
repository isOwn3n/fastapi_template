from http import HTTPStatus
from fastapi import HTTPException
from .base import BaseRepository
from models import RevokeToken
from sqlmodel import select, delete
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import pytz


class TokenRepository(BaseRepository):
    async def revoke_token(self, token: str):
        s = select(RevokeToken).where(RevokeToken.token == token)
        try:
            print("First:", (await self.session.exec(s)).first())
            if (await self.session.exec(s)).first():
                raise HTTPException(HTTPStatus.UNAUTHORIZED)
            return True
        except NoResultFound:
            return True

    async def delete_exp_token(self):
        await self.session.exec(
            delete(RevokeToken).where(
                RevokeToken.rev_date
                < datetime.now().replace(tzinfo=pytz.timezone("Asia/Tehran"))
            )
        )
        await self.session.commit()
