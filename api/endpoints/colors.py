from uuid import UUID
from enum import Enum
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.authentication import create_access_token, get_password_hash, verify_password
from api.exceptions.common import ForbiddenException
from api.schemas.common import SuccessfullResponse, TokenOut
from migrations.database.connection.session import get_session
from migrations.database.models.credentials import CredentialTypes
from api.services.auth import add_new_user, get_user_by_email_or_phone
from api.schemas.auth import UserRegister, UserLoginBasic
from api.exceptions.common import BadRequest
from api.schemas.colors import ColorStage, Color, ColorStages
from migrations.database.models.events import LogoVariant
from migrations.database.models.participations import ParticipationStages


color_router = APIRouter(tags=["Цветовые вариации"])


@color_router.get("/colors", response_model=list[Color])
async def get_color_by_variant(
    color_stage: ColorStage = Depends(),
    session: AsyncSession = Depends(get_session),
) -> list[Color]:
    stage_to_color = {
        ParticipationStages.NOT_PARTICIPATED: ColorVariant.ORANGE,
        ParticipationStages.PAYMENT_PENDING: ColorVariant.YELLOW,
        ParticipationStages.PAYMENT_NEEDED: ColorVariant.RED,
        ParticipationStages.APPROVED: ColorVariant.GREEN,
        ParticipationStages.DECLINED: ColorVariant.GRAY
    }
    color = stage_to_color[color_stage.stage.value].lower()
    return [
        Color(type=LogoVariant.SCOUT, file_id=f'static/1-{color}.png'),
        Color(type=LogoVariant.CAMP, file_id=f'static/2-{color}.png'),
        Color(type=LogoVariant.FOREST, file_id=f'static/3-{color}.png'),
        Color(type=LogoVariant.TRIPLE_DANCING, file_id=f'static/4-{color}.png'),
        Color(type=LogoVariant.PAIR_STANDING, file_id=f'static/5-{color}.png'),
        Color(type=LogoVariant.TRIPLE_STANDING, file_id=f'static/6-{color}.png'),
        Color(type=LogoVariant.TRIPLE_SITTING, file_id=f'static/7-{color}.png'),
    ]

