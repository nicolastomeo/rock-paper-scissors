from typing import Optional

import sqlalchemy.exc
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.exceptions import GameNotFound
from app.exceptions import InvalidTurn
from app.exceptions import TurnNotFound
from app.models import Move


class TurnsRepository:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def create_turn(self, game_id: int) -> models.Turn:
        db_turn = models.Turn(game_id=game_id)
        self._db_session.add(db_turn)
        try:
            await self._db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise GameNotFound()
        await self._db_session.refresh(db_turn)
        return db_turn

    async def get_turn(self, game_id: int, turn_id: int) -> models.Turn:
        turn_result = await self._db_session.execute(
            select(models.Turn).filter(
                models.Turn.id == turn_id, models.Turn.game_id == game_id
            )
        )
        return turn_result.scalar()

    async def update_turn(
        self,
        game_id: int,
        turn_id: int,
        player_one_move: Optional[Move],
        player_two_move: Optional[Move],
    ):
        # Lock turn row to avoid concurrent updates
        turn_result = await self._db_session.execute(
            select(models.Turn)
            .filter(models.Turn.id == turn_id, models.Turn.game_id == game_id)
            .with_for_update()
        )
        turn: models.Turn = turn_result.scalar()
        if turn is None:
            raise TurnNotFound()
        if player_one_move is not None:
            if turn.player_one_move is not None:
                raise InvalidTurn()
            turn.player_one_move = player_one_move
        if player_two_move is not None:
            if turn.player_two_move is not None:
                raise InvalidTurn()
            turn.player_two_move = player_two_move
        if turn.player_one_move is not None and turn.player_two_move is not None:
            if player_one_move is not None or player_two_move is not None:
                player_one_result, _ = turn.calc_player_results()
                if player_one_result == models.Result.WIN:
                    update_values = {
                        "player_one_score": models.Game.player_one_score + 1
                    }
                elif player_one_result == models.Result.LOSE:
                    update_values = {
                        "player_two_score": models.Game.player_two_score + 1
                    }
                else:
                    update_values = {
                        "player_one_score": models.Game.player_one_score + 1,
                        "player_two_score": models.Game.player_two_score + 1,
                    }
                # Execute atomic increment
                await self._db_session.execute(
                    update(models.Game)
                    .filter(models.Game.id == game_id)
                    .values(update_values)
                )
        await self._db_session.commit()
        return turn
