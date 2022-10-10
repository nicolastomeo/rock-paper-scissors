from typing import Optional

from pydantic.class_validators import root_validator
from pydantic.main import BaseModel

from app.models import Move
from app.models import Result


class Turn(BaseModel):
    id: int
    game_id: int
    player_one_move: Optional[Move]
    player_two_move: Optional[Move]

    class Config:
        orm_mode = True


class TurnUpdate(BaseModel):
    player_one_move: Optional[Move]
    player_two_move: Optional[Move]

    @root_validator
    def check_at_least_one_move(cls, values):
        one, two = values.get("player_one_move"), values.get("player_two_move")
        if one is None and two is None:
            raise ValueError(
                "player_one_move and player_two_move can not be null simultaneously"
            )
        return values


class TurnResult(BaseModel):
    player_one_result: Optional[Result]
    player_two_result: Optional[Result]
