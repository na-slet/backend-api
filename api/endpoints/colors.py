from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.colors import ColorStage, Color, ColorVariants
from database.connection.session import get_session
from database.models.events import LogoVariant
from database.models.participations import ParticipationStages

color_router = APIRouter(tags=["Цветовые вариации"])


@color_router.get("/colors", response_model=list[Color])
async def get_color_by_variant(
        color_stage: ColorStage = Depends(),
        session: AsyncSession = Depends(get_session),
) -> list[Color]:
    stage_to_color = {
        ParticipationStages.NOT_PARTICIPATED: ColorVariants.ORANGE,
        ParticipationStages.PAYMENT_PENDING: ColorVariants.YELLOW,
        ParticipationStages.PAYMENT_NEEDED: ColorVariants.RED,
        ParticipationStages.APPROVED: ColorVariants.GREEN,
        ParticipationStages.DECLINED: ColorVariants.GRAY
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

