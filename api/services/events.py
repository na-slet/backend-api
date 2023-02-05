import sqlalchemy
import os
from migrations.database.models import Users, Events, Participations, Unions
from migrations.database.models.events import Visibility
from migrations.database.models.participations import ParticipationStages
import hashlib
from api.exceptions.common import BadRequest, NotFoundException, InternalServerError

from api.schemas.users import UserProfile
from api.schemas.common import TokenIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, or_, insert
from sqlalchemy.orm import aliased
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from api.utils.formatter import combine_models
from api.schemas.events import EventSearch, EventOut, EventIn, PaymentPhoto, UserEventUpdate

from uuid import UUID

from migrations.database.models import Users, Events, Participations
from migrations.database.models.credentials import CredentialTypes

from api.exceptions.common import BadRequest, NotFoundException, InternalServerError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, and_, or_,delete, update
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from api.schemas.events import EventIn, EventNew, UserEvent, EventOut, UserEventKick, EventInOptional


async def get_user_event(user: Users, event: EventIn, session: AsyncSession) -> Events:
    try:
        query = select(Events).where(
            and_(
                Events.id == str(event.id),
                Events.creator_id == str(user.id)
            )
        )
        result = (await session.execute(query)).scalars().first()
        if not result:
            raise NotFoundException("Event not found")
        return result
    except IntegrityError as e:
        raise InternalServerError(e) from e


async def get_user_events(user: Users, session: AsyncSession, event_id: UUID = None) -> list[Events]:
    try:
        query = select(Events).where(
            Events.creator_id == str(user.id)
        )
        if event_id:
            query.where(Events.id == str(event_id))
        result = (await session.execute(query)).scalars().all()
        return result
    except IntegrityError as e:
        raise InternalServerError(e) from e


async def get_event_users(user: Users, event: EventIn, session: AsyncSession) -> list[(Users,Participations)]:
    query = select(Users, Participations).join(
        Participations, Users.id == Participations.user_id
    ).join(
        Events, Events.id == Participations.event_id
    ).where(
        and_(
            Participations.event_id == str(event.id),
            Events.creator_id == str(user.id)
        )
    )
    return (await session.execute(query)).all()


async def create_new_event(user: Users, event: EventNew, session: AsyncSession) -> None:
    try:
        query = insert(Events).values(
            name=event.name,
            description=event.description,
            short_description=event.short_description,
            **({'visibility': event.visibility} if event.visibility else {}),
            price=event.price,
            logo_variant=event.logo_variant,
            city=event.city,
            reg_end_date=event.reg_end_date,
            start_date=event.start_date,
            end_date=event.end_date,
            total_places=event.total_places,
            url_link=event.url_link,
            category_type=event.category_type,
            event_type=event.event_type,
            **({'union_id': str(event.union_id)} if event.union_id else {}),
            min_age=event.min_age,
            max_age=event.max_age,
            address=event.address,
            latitude=event.latitude,
            longitude=event.longitude,
            creator_id=str(user.id)
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise InternalServerError(e) from e


async def delete_event(user: Users, user_event: EventIn, session: AsyncSession) -> None:
    try:
        query = delete(Events).where(and_(
            Events.id == str(user_event.id),
            Events.creator_id == str(user.id)
        ))
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise InternalServerError(e) from e


async def change_participation_status(creator: Users, user_event: UserEventUpdate, session: AsyncSession) -> None:
    try:
        query = update(Participations).values(
            participation_stage=user_event.stage
        ).where(and_(
            Participations.user_id == str(user_event.user_id),
            Participations.event_id == str(user_event.event_id),
            Participations.event_id.in_(select(Events.id).where(Events.creator_id == creator.id))
        )).execution_options(synchronize_session="fetch")
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise InternalServerError(e) from e


async def kick_user_from_participation(creator: Users, user_event_kick: UserEventKick, session: AsyncSession) -> None:
    try:
        query = delete(Participations).where(and_(
          Participations.event_id == str(user_event_kick.event_id),
          Participations.user_id == str(user_event_kick.user_id),
          Participations.event_id.in_(select(Events.id).where(Events.creator_id == creator.id))
        )).execution_options(synchronize_session="fetch")
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise InternalServerError(e) from e

async def update_event(user: Users, user_event: EventOut, session: AsyncSession) -> None:
    try:
        query = update(Events).values(
            name=func.coalesce(user_event.name, Events.name),
            description=func.coalesce(user_event.description, Events.description),
            short_description=func.coalesce(user_event.short_description, Events.short_description),
            visibility=func.coalesce(user_event.visibility, Events.visibility),
            price=func.coalesce(user_event.price, Events.price),
            logo_variant=func.coalesce(user_event.logo_variant, Events.logo_variant),
            city=func.coalesce(user_event.city, Events.city),
            reg_end_date=func.coalesce(user_event.reg_end_date, Events.reg_end_date),
            start_date=func.coalesce(user_event.start_date, Events.start_date),
            end_date=func.coalesce(user_event.end_date, Events.end_date),
            total_places=func.coalesce(user_event.total_places, Events.total_places),
            url_link=func.coalesce(user_event.url_link, Events.url_link),
            category_type=func.coalesce(user_event.category_type, Events.category_type),
            event_type=func.coalesce(user_event.event_type, Events.event_type),
            union_id=func.coalesce(user_event.union_id, Events.union_id),
            min_age=func.coalesce(user_event.min_age, Events.min_age),
            max_age=func.coalesce(user_event.max_age, Events.max_age),
            address=func.coalesce(user_event.address, Events.address),
            latitude=func.coalesce(user_event.latitude, Events.latitude),
            longitude=func.coalesce(user_event.longitude, Events.longitude),
        ).where(and_(
            Events.creator_id == str(user.id),
            Events.id == str(user_event.id)
        ))
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise InternalServerError(e) from e

async def search_events(event_search: EventSearch, user: Users, session: AsyncSession) -> list[(Events, Unions)]:
    subquery = select(Participations).where(and_(
        Participations.user_id == user.id
    )).limit(1).cte()
    subquery = aliased(Participations, subquery)
    query = select(Events, Unions, subquery). \
        join(Unions, Events.union_id == Unions.id, isouter=True). \
        join(subquery, Events.id == subquery.event_id, isouter=True). \
        where(and_(
            Events.reg_end_date > event_search.reg_start_date if event_search.reg_start_date else True,
            Events.reg_end_date > event_search.reg_end_date if event_search.reg_end_date else True,
            Events.start_date > event_search.start_date if event_search.start_date else True,
            Events.end_date > event_search.end_date if event_search.end_date else True,
            Events.category_type > event_search.category_type if event_search.category_type else True,
            Events.event_type > event_search.event_type if event_search.event_type else True,
            Events.visibility == Visibility.PUBLIC
        ))
        # group_by(Events.id, Unions.id, subquery.id, subquery.user_id, subquery.event_id, subquery.participation_stage, subquery.payment_id, subquery.created_at)
    events = (await session.execute(query)).all()
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
    fname = None
    if payment.payment: # TODO: заставить влада кидать фотки
        data = payment.payment.file.read()
        filetype = os.path.splitext(payment.payment.filename)[-1]
        fname = f'static/{hashlib.sha224(data).hexdigest()}{filetype}'
        with open(fname, mode='wb+') as f:
            f.write(data)
    try:
        query = update(Participations).values(
            participation_stage=ParticipationStages.PAYMENT_PENDING,
            payment_id=fname
        ).where(and_(
            Participations.user_id == str(user.id),
            Participations.event_id == str(payment.event_id),
        ))
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise InternalServerError(e) from e
