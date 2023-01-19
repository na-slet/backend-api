
from migrations.database.models import Users, Credentials
from migrations.database.models.credentials import CredentialTypes

from api.exceptions.common import BadRequest, NotFoundException, InternalServerError
from api.schemas.auth import UserUpdate, UserRegister, UserLoginBasic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy import select, insert, and_, or_, update
from sqlalchemy.exc import IntegrityError
from migrations.database.models import Unions


async def get_unions(session: AsyncSession) -> list[Unions]:
    query = select(Unions)
    result = (await session.execute(query)).scalars().all()
    return result
