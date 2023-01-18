from uuid import UUID
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.authentication import create_access_token, get_password_hash, verify_password
from api.exceptions.common import ForbiddenException
from api.schemas.common import SuccessfullResponse, TokenOut
from migrations.database.connection.session import get_session
from migrations.database.models.credentials import CredentialTypes
from api.services.auth import add_new_user, get_user_by_email_or_phone
from api.schemas.auth import UserRegister, UserLoginBasic


auth_router = APIRouter(tags=["Аутентификация"])


@auth_router.post("/user/register", response_model=SuccessfullResponse)
async def register_new_user(
    session: AsyncSession = Depends(get_session),
    user_register: UserRegister = Depends()
) -> SuccessfullResponse:
    user_register.password = get_password_hash(user_register.password)
    await add_new_user(user_register, CredentialTypes.BASIC, session)
    return SuccessfullResponse()


@auth_router.post("/user/login", response_model=TokenOut)
async def log_user_in(user_login: UserLoginBasic = Depends(),
                     session: AsyncSession = Depends(get_session)) -> TokenOut:
    credential = await get_user_by_email_or_phone(user_login, session)
    if not verify_password(user_login.password, credential.value):
        raise ForbiddenException("Wrong password")
    access_token = create_access_token(data={"sub": user_login.identity})
    token = TokenOut(access_token=access_token, token_type="bearer")
    return token
