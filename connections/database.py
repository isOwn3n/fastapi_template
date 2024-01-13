from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from settings import config


engine = create_async_engine(
    config.database_url,
    connect_args=config.database_connection_args,
    echo=config.debug
)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session