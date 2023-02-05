from sqlalchemy import select, insert, and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions.common import BadRequest, NotFoundException, InternalServerError
from api.schemas.auth import UserRegister, UserLoginBasic
from migrator.models import Users, Credentials
from migrator.models.credentials import CredentialTypes


async def add_new_user(user_register: UserRegister, credential_type: str, session: AsyncSession) -> None:
    try:
        query = insert(Users).values(
            email=user_register.email,
            **({'role': user_register.role} if user_register.role else {})
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
        await session.rollback()
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
