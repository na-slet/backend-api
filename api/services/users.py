from sqlalchemy import func
from sqlalchemy import select, update, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions.common import NotFoundException, InternalServerError
from api.schemas.users import UserProfile
from database.models import Users


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
    # fname = None
    # if user_profile.avatar:
    #     data = user_profile.avatar.file.read()
    #     filetype = os.path.splitext(user_profile.avatar.filename)[-1]
    #     fname = f'static/{hashlib.sha224(data).hexdigest()}{filetype}'
    #     with open(fname, mode='wb+') as f:
    #         f.write(data)
    try:
        query = update(Users).values(
            first_name=func.coalesce(user_profile.first_name, Users.first_name),
            middle_name=func.coalesce(user_profile.middle_name, Users.middle_name),
            last_name=func.coalesce(user_profile.last_name, Users.last_name),
            gender=func.coalesce(user_profile.gender, Users.gender),
            phone=func.coalesce(user_profile.phone, Users.phone),
            parent_phone=func.coalesce(user_profile.parent_phone, Users.parent_phone),
            parent_fio=func.coalesce(user_profile.parent_fio, Users.parent_fio),
            parent_email=func.coalesce(user_profile.parent_email, Users.parent_email),
            email=func.coalesce(user_profile.email, Users.email),
            # avatar_id=func.coalesce(fname, Users.avatar_id),
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

