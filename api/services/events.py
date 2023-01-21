import sqlalchemy
import os
from migrations.database.models import Users, Events, Participations
import hashlib
from api.exceptions.common import BadRequest, NotFoundException, InternalServerError

from api.schemas.users import UserProfile
from api.schemas.common import TokenIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, or_, insert
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from api.utils.formatter import combine_models
from api.schemas.events import EventSearch, EventOut, EventIn, PaymentPhoto


async def search_events(event_search: EventSearch, session: AsyncSession) -> list[Events]:
    query = select(Events).where(and_(
        Events.reg_end_date > event_search.reg_start_date if event_search.reg_start_date else True,
        Events.reg_end_date > event_search.reg_end_date if event_search.reg_end_date else True,
        Events.start_date > event_search.start_date if event_search.start_date else True,
        Events.end_date > event_search.end_date if event_search.end_date else True,
        Events.category_type > event_search.category_type if event_search.category_type else True,
        Events.event_type > event_search.event_type if event_search.event_type else True
    ))
    events = (await session.execute(query)).scalars().all()
    return events


async def get_participations(identity: str, session: AsyncSession) -> list[(Events, Participations)]:
    query = select(Events, Participations).join(
        Participations, Events.id == Participations.event_id
    ).join(
        Users, Participations.user_id == Users.id
    ).where(
        or_(
            Users.email == identity,
            Users.phone == identity
        )
    )
    return (await session.execute(query)).all()


async def user_participate(event_in: EventIn, user: Users, session: AsyncSession) -> None:
    try:
        query = insert(Participations).values(
            user_id=str(user.id),
            event_id=str(event_in.id),
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise BadRequest('Already participated or Event not found', e) from e


async def user_payment_send(payment: PaymentPhoto, user: Users, session: AsyncSession) -> None:
    data = payment.payment.file.read()
    filetype = os.path.splitext(payment.payment.filename)[-1]
    fname = f'static/{hashlib.sha224(data).hexdigest()}{filetype}'
    with open(fname, mode='wb+') as f:
        f.write(data)
    try:
        query = update(Participations).values(
            payment_id=fname
        ).where(
            Participations.user_id == str(user.id),
            Participations.event_id == str(payment.event_id),
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise InternalServerError(e) from e
