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
from api.schemas.events import EventOut, EventSearch, UserEvent
from api.services.unions import get_unions
from api.utils.formatter import serialize_models
from api.schemas.unions import Union

union_router = APIRouter(tags=["Объединения"])


@union_router.get("/unions", response_model=list[Union])
async def get_all_unions(
    session: AsyncSession = Depends(get_session),
) -> list[Union]:
    unions_raw = await get_unions(session)
    return serialize_models(unions_raw, Union)


