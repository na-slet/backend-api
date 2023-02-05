from datetime import datetime

from fastapi import APIRouter
from fastapi.param_functions import Depends
from pytz import UTC
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions.common import BadRequest
from api.schemas.common import SuccessfullResponse
from api.schemas.events import EventOut, FoundEvent, EventSearch, PaymentPhoto, UserParticipation, EventIn, \
    Participation
from api.schemas.events import UserRequiredAdult, UserRequiredChild
from api.schemas.unions import Union
from api.services.events import search_events, get_participations, user_participate, user_payment_send
from api.services.users import get_user_by_identity
from api.utils.authentication import get_user_identity
from migrator.connection.session import get_session
from migrator.models.participations import ParticipationStages

event_router = APIRouter(tags=["Функции слётов"])


@event_router.get("/events", response_model=list[FoundEvent])
async def search_for_events(
    event_search: EventSearch = Depends(),
    session: AsyncSession = Depends(get_session),
    identity: str = Depends(get_user_identity)
) -> list[FoundEvent]:
    user = await get_user_by_identity(identity, session)
    events = await search_events(event_search, user, session)
    result = list()
    for el in events:
        event, union, participation = el
        event, union, participation = EventOut.from_orm(event), Union.from_orm(union), Participation.from_orm(participation)
        participation.participation_stage = participation.participation_stage or ParticipationStages.NOT_PARTICIPATED
        result.append(FoundEvent(event=event, union=union, participation=participation))
    return result


@event_router.get("/user/events", response_model=list[UserParticipation])
async def get_user_participation(
    session: AsyncSession = Depends(get_session),
    identity: str = Depends(get_user_identity)
) -> list[UserParticipation]:
    participations = await get_participations(identity, session)
    result = list()
    for el in participations:
        event, participation = el
        event, participation = EventOut.from_orm(event), Participation.from_orm(participation)
        result.append(UserParticipation(event=event, participation=participation))
    return result


@event_router.post('/event', response_model=SuccessfullResponse)
async def participate_in_event(
    event_in: EventIn,
    identity: str = Depends(get_user_identity),
    session: AsyncSession = Depends(get_session),
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    try:
        if user.birth_date and (datetime.now(tz=UTC) - user.birth_date).days < 18*365:
            UserRequiredChild.from_orm(user)
        else:
            UserRequiredAdult.from_orm(user)
    except Exception as e:
        raise BadRequest('Profile is not completely filled', e) from e
    await user_participate(event_in, user, session)
    return SuccessfullResponse()


@event_router.post('/user/event/payment', response_model=SuccessfullResponse)
async def send_payment_photo(
    payment: PaymentPhoto = Depends(),
    identity: str = Depends(get_user_identity),
    session: AsyncSession = Depends(get_session),
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await user_payment_send(payment, user, session)
    return SuccessfullResponse()
