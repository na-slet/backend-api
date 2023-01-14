import sqlalchemy

from migrations.database.models import Users, Credentials
from migrations.database.models.credentials import CredentialTypes

from api.exceptions.common import BadRequest, NotFoundException, InternalServerError

from api.schemas.users import UserProfile
from api.schemas.common import TokenIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, or_
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError


async def get_user_by_identity(identity: str, session: AsyncSession) -> Users:
    try:
        query = select(Users).where(
            or_(
                Users.email == identity,
                Users.phone == identity
            )
        )
        user = (await session.execute(query)).scalars().first()
        if not user:
            raise NotFoundException("User not found")
        return user
    except IntegrityError as e:
        raise InternalServerError(e) from e


async def update_user_profile(user_profile: UserProfile, user: Users, session: AsyncSession) -> None:
    try:
        query = update(Users).values(
            first_name=func.coalesce(user_profile.first_name, Users.first_name),
            last_name=func.coalesce(user_profile.last_name, Users.last_name),
            gender=func.coalesce(user_profile.gender, Users.gender),
            phone=func.coalesce(user_profile.phone, Users.phone),
            email=func.coalesce(user_profile.email, Users.email),
            avatar_id=func.coalesce(user_profile.avatar, Users.avatar_id),
            city=func.coalesce(user_profile.city, Users.city),
            tg_link=func.coalesce(user_profile.tg_link, Users.tg_link),
            birth_date=func.coalesce(user_profile.birth_date, Users.birth_date),
        ).where(
            Users.id == user.id
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise InternalServerError(e) from e
