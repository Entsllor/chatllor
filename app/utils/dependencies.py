from app.core.database import async_session, AsyncSession


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
