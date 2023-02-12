from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.unions import Union
from api.services.unions import get_unions
from api.utils.formatter import serialize_models
from database.connection.session import get_session

union_router = APIRouter(tags=["Объединения"])


@union_router.get("/unions", response_model=list[Union])
async def get_all_unions(
    session: AsyncSession = Depends(get_session),
) -> list[Union]:
    unions_raw = await get_unions(session)
    return serialize_models(unions_raw, Union)


