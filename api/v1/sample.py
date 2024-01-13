from repository import SampleRepository
from schema import SampleGetResponse
from connections import get_session # type: ignore
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.routing import APIRouter
from typing import Annotated
from fastapi import Query, Depends


sample_router = APIRouter()

@sample_router.get("/")
def read_sample(session: Annotated[AsyncSession, Depends(get_session)], limit: int = Query(default=100, le=100), offset: int = 0):
    repo = SampleRepository(session)
    return repo.list(limit, offset)