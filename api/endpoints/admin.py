from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.common import SuccessfullResponse
from api.schemas.events import EventOut, EventIn, UserEventUpdate, EventNew, Participation, UserEventKick, \
    EventInOptional
from api.schemas.users import UserOut, UserParticipation
from api.services.events import get_user_event, get_event_users, get_user_events, create_new_event, delete_event, \
    update_event, change_participation_status, kick_user_from_participation
from api.services.users import get_user_by_identity
from api.utils.authentication import get_user_identity
from api.utils.formatter import serialize_models
from database.connection.session import get_session

admin_router = APIRouter(tags=["Функции создателя"], prefix='/admin')


@admin_router.get("/event/users", response_model=list[UserParticipation])
async def get_users_on_event(
    identity: str = Depends(get_user_identity),
    event: EventIn = Depends(),
    session: AsyncSession = Depends(get_session),
) -> list[UserParticipation]:
    user = await get_user_by_identity(identity,session)
    event = await get_user_event(user, event, session)
    users = await get_event_users(user, event, session)
    result = list()
    print(users)
    for el in users:
        user, participation = el
        user, participation = UserOut.from_orm(user), Participation.from_orm(participation)
        result.append(UserParticipation(user=user, participation=participation))
    return result


@admin_router.post("/event", response_model=SuccessfullResponse)
async def create_event(
    identity: str = Depends(get_user_identity),
    event_new: EventNew = Depends(),
    session: AsyncSession = Depends(get_session),
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await create_new_event(user, event_new, session)
    return SuccessfullResponse()


@admin_router.delete('/event', response_model=SuccessfullResponse)
async def delete_event_by_id(
    identity: str = Depends(get_user_identity),
    event_in: EventIn = Depends(),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await delete_event(user, event_in, session)
    return SuccessfullResponse()


@admin_router.put("/user/event/status", response_model=SuccessfullResponse)
async def change_payment_status(
    user_event: UserEventUpdate,
    identity: str = Depends(get_user_identity),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await change_participation_status(user, user_event, session)
    return SuccessfullResponse()

@admin_router.post("/user/event/kick", response_model=SuccessfullResponse)
async def kick_user(
    user_event_kick: UserEventKick,
    identity: str = Depends(get_user_identity),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await kick_user_from_participation(user, user_event_kick, session)
    return SuccessfullResponse()


@admin_router.put("/user/event", response_model=SuccessfullResponse)
async def update_user_event(
    user_event: EventOut,
    identity: str = Depends(get_user_identity),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await update_event(user, user_event, session)
    return SuccessfullResponse()


@admin_router.get('/user/events', response_model=list[EventOut])
async def get_created_events(
    identity: str = Depends(get_user_identity),
    event_id: EventInOptional = Depends(),
    session: AsyncSession = Depends(get_session)
) -> list[EventOut]:
    user = await get_user_by_identity(identity, session)
    events = await get_user_events(user, session, event_id.id)
    return serialize_models(events, EventOut)
