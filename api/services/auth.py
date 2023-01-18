
from migrations.database.models import Users, Credentials
from migrations.database.models.credentials import CredentialTypes

from api.exceptions.common import BadRequest, NotFoundException, InternalServerError
from api.schemas.auth import UserUpdate, UserRegister, UserLoginBasic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy import select, insert, and_, or_, update
from sqlalchemy.exc import IntegrityError


async def add_new_user(user_register: UserRegister, credential_type: str, session: AsyncSession) -> None:
    try:
        query = insert(Users).values(
            email=user_register.email,
        ).returning(Users.id)
        user_id = (await session.execute(query)).scalars().first()
        query = insert(Credentials).values(
            user_id=user_id,
            credential_type=credential_type,
            value=user_register.password,
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise BadRequest("User already exist", e) from e


async def get_user_by_email_or_phone(user_login: UserLoginBasic, session: AsyncSession) -> Credentials:
    try:
        query = select(Credentials).join(Users, Users.id == Credentials.user_id).where(
            and_(
                Credentials.credential_type == CredentialTypes.BASIC,
                or_(
                    Users.email == user_login.identity,
                    Users.phone == user_login.identity
                )
            )
        )
        result = (await session.execute(query)).scalars().first()
        if not result:
            raise NotFoundException("User not found")
        return result
    except IntegrityError as e:
        raise InternalServerError(e) from e
