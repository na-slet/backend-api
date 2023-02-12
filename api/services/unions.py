from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Unions


async def get_unions(session: AsyncSession) -> list[Unions]:
    query = select(Unions)
    result = (await session.execute(query)).scalars().all()
    return result
