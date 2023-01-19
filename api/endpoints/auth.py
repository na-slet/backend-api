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


@auth_router.post("/user/auth", response_model=TokenOut)
async def authenticate_user_if_present_otherwise_register(
    session: AsyncSession = Depends(get_session),
    user_register: UserRegister = Depends()
) -> TokenOut:
    user_login = UserLoginBasic(identity=user_register.email, password=user_register.password)
    user_register.password = get_password_hash(user_register.password)
    await add_new_user(user_register, CredentialTypes.BASIC, session)
    credential = await get_user_by_email_or_phone(user_login, session)
    if not verify_password(user_login.password, credential.value):
        raise ForbiddenException("Wrong password")
    access_token = create_access_token(data={"sub": user_register.email})
    token = TokenOut(access_token=access_token, token_type="bearer")
    return token
