from uuid import UUID
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.authentication import create_access_token, get_password_hash, verify_password, get_current_user
from api.exceptions.common import ForbiddenException
from api.schemas.common import SuccessfullResponse, TokenOut
from migrations.database.connection.session import get_session
from api.services.auth import add_new_user, get_user, add_task_for_verification
from api.schemas.auth import UserIn

auth_router = APIRouter(tags=["Аутентификация"])


@auth_router.post("/user/register", response_model=SuccessfullResponse)
async def user_register(
    request: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    request.password = get_password_hash(request.password)
    await add_new_user(request.username, request.password, session)
    await add_task_for_verification(request.username, session)
    return SuccessfullResponse()


@auth_router.post("/user/login", response_model=TokenOut)
async def user_login(request: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_session)) -> TokenOut:
    user = await get_user(request.username, session)
    if not verify_password(request.password, user.hashed_password):
        raise ForbiddenException("Wrong password")
    access_token = create_access_token(data={"sub": user.phone})
    token = TokenOut(access_token=access_token, token_type="bearer")
    return token