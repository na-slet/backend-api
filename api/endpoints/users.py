from uuid import UUID
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.authentication import create_access_token, get_password_hash, verify_password, get_user_identity
from api.exceptions.common import ForbiddenException
from api.schemas.common import SuccessfullResponse, TokenOut, TokenIn
from migrations.database.connection.session import get_session
from migrations.database.models.credentials import CredentialTypes
from api.services.auth import add_new_user, get_user_by_email_or_phone
from api.services.users import get_user_by_identity, update_user_profile
from api.schemas.users import UserProfile


user_router = APIRouter(tags=["Функции пользователя"])


@user_router.put("/user", response_model=SuccessfullResponse)
async def user_register(
    session: AsyncSession = Depends(get_session),
    user_profile: UserProfile = Depends(),
    identity: str = Depends(get_user_identity)
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await update_user_profile(user_profile,user,session)
    return SuccessfullResponse()


@user_router.get("/user", response_model=UserProfile)
async def user_login(
    session: AsyncSession = Depends(get_session),
    identity: str = Depends(get_user_identity)
) -> UserProfile:
    user = await get_user_by_identity(identity, session)
    return UserProfile.from_orm(user)
