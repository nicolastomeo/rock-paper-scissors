from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.games.schemas import GameCreate


class GamesRepository:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def create_game(self, game_create: GameCreate) -> models.Game:
        db_game = models.Game(
            player_one=game_create.player_one, player_two=game_create.player_two
        )
        self._db_session.add(db_game)
        await self._db_session.commit()
        await self._db_session.refresh(db_game)
        return db_game

    async def get_game(self, game_id) -> models.Game:
        result = await self._db_session.execute(
            select(models.Game).filter(models.Game.id == game_id)
        )
        return result.scalar()
