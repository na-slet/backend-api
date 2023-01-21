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
from api.schemas.events import EventOut, EventSearch, PaymentPhoto, UserParticipation, EventIn, Participation
from api.services.events import search_events, get_participations, user_participate, user_payment_send
from api.utils.formatter import serialize_models


event_router = APIRouter(tags=["Функции пользователя"])


@event_router.get("/events", response_model=list[EventOut])
async def search_for_events(
    session: AsyncSession = Depends(get_session),
    event_search: EventSearch = Depends(),
) -> list[EventOut]:
    events = await search_events(event_search, session)
    return serialize_models(events, EventOut)


@event_router.get("/user/events", response_model=list[UserParticipation])
async def get_user_participation(
    session: AsyncSession = Depends(get_session),
    identity: str = Depends(get_user_identity)
) -> list[EventOut]:
    participations = await get_participations(identity, session)
    result = list()
    for el in participations:
        event, participation = el
        event, participation = EventOut.from_orm(event), Participation.from_orm(participation)
        result.append(UserParticipation(event=event, participation=participation))
    return result



@event_router.post('/event', response_model=SuccessfullResponse)
async def participate_in_event(
        session: AsyncSession = Depends(get_session),
        event_in: EventIn = Depends(),
        identity: str = Depends(get_user_identity)
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await user_participate(event_in, user, session)
    return SuccessfullResponse()


@event_router.post('/user/event/payment', response_model=SuccessfullResponse)
async def send_payment_photo(
    session: AsyncSession = Depends(get_session),
    payment: PaymentPhoto = Depends(),
    identity: str = Depends(get_user_identity)
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await user_payment_send(payment, user, session)
    return SuccessfullResponse()