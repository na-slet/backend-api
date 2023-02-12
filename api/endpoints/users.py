from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.common import SuccessfullResponse
from api.schemas.users import UserProfile, UserOut
from api.services.users import get_user_by_identity, update_user_profile
from api.utils.authentication import get_user_identity
from database.connection.session import get_session

user_router = APIRouter(tags=["Функции пользователей"])


@user_router.put("/user", response_model=SuccessfullResponse)
async def update_user(
    user_profile: UserProfile,
    identity: str = Depends(get_user_identity),
    session: AsyncSession = Depends(get_session),
) -> SuccessfullResponse:
    user = await get_user_by_identity(identity, session)
    await update_user_profile(user_profile,user,session)
    return SuccessfullResponse()


@user_router.get("/user", response_model=UserOut)
async def get_user(
    session: AsyncSession = Depends(get_session),
    identity: str = Depends(get_user_identity)
) -> UserOut:
    user = await get_user_by_identity(identity, session)
    user_out = UserOut.from_orm(user)
    return user_out
