import sqlalchemy
import os
import hashlib
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
    fname = None
    if user_profile.avatar:
        data = user_profile.avatar.file.read()
        filetype = os.path.splitext(user_profile.avatar.filename)[-1]
        fname = f'static/{hashlib.sha224(data).hexdigest()}{filetype}'
        with open(fname, mode='wb+') as f:
            f.write(data)
    if user_profile.parent_fio:
        try:
            last_name,first_name,middle_name = user_profile.parent_fio.split()
            user_profile.parent_last_name = last_name
            user_profile.parent_middle_name = middle_name
            user_profile.parent_first_name = first_name
        except Exception as e:
            raise BadRequest('Parent fio should consist of last_name, first_name, middle_name',e) from e
    try:
        query = update(Users).values(
            first_name=func.coalesce(user_profile.first_name, Users.first_name),
            middle_name=func.coalesce(user_profile.middle_name, Users.middle_name),
            last_name=func.coalesce(user_profile.last_name, Users.last_name),
            gender=func.coalesce(user_profile.gender, Users.gender),
            phone=func.coalesce(user_profile.phone, Users.phone),
            parent_phone=func.coalesce(user_profile.parent_phone, Users.parent_phone),
            parent_first_name=func.coalesce(user_profile.parent_first_name, Users.parent_first_name),
            parent_middle_name=func.coalesce(user_profile.parent_middle_name, Users.parent_middle_name),
            parent_last_name=func.coalesce(user_profile.parent_last_name, Users.parent_last_name),
            parent_email=func.coalesce(user_profile.parent_email, Users.parent_email),
            email=func.coalesce(user_profile.email, Users.email),
            avatar_id=func.coalesce(fname, Users.avatar_id),
            city=func.coalesce(user_profile.city, Users.city),
            tg_link=func.coalesce(user_profile.tg_link, Users.tg_link),
            union_id=func.coalesce(user_profile.union_id, Users.union_id),
            birth_date=func.coalesce(user_profile.birth_date, Users.birth_date),
        ).where(
            Users.id == user.id
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise NotFoundException('Union not found') from e

