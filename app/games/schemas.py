from typing import Optional

from pydantic.main import BaseModel


class GameCreate(BaseModel):
    player_one: str
    player_two: Optional[str]


class Game(GameCreate):
    id: int
    player_one_score: int
    player_two_score: int

    class Config:
        orm_mode = True
