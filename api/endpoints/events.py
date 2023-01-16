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


user_router = APIRouter(tags=["Функции пользователя"])


@user_router.get("/events", response_model=list[EventOut])
async def get_(
    session: AsyncSession = Depends(get_session),
    event_search: EventSearch = Depends(),
    identity: str = Depends(get_user_identity)
) -> list[EventOut]:
    pass


@user_router.get("/user/events", response_model=list[EventOut])
async def user_login(
    session: AsyncSession = Depends(get_session),
    user_event: UserEvent = Depends(),
    identity: str = Depends(get_user_identity)
) -> list[EventOut]:
    pass
