from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session
from app.turns.repository import TurnsRepository


def get_turns_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> TurnsRepository:
    return TurnsRepository(db_session)
