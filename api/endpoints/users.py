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
from api.schemas.auth import UserUpdate
from api.schemas.users import UserProfile, UserOut


user_router = APIRouter(tags=["Функции пользователей"])


@user_router.put("/user", response_model=SuccessfullResponse)
async def update_user(
    user_profile: UserProfile,
    identity: str = Depends(get_user_identity),
    session: AsyncSession = Depends(get_session),
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await update_user_profile(user_profile,user,session)
    return SuccessfullResponse()


@user_router.get("/user", response_model=UserOut)
async def get_user(
    session: AsyncSession = Depends(get_session),
    identity: str = Depends(get_user_identity)
) -> UserOut:
    user = await get_user_by_identity(identity, session)
    return UserOut.from_orm(user)
