from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session
from app.games.repository import GamesRepository


def get_games_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> GamesRepository:
    return GamesRepository(db_session)
