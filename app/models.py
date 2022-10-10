import enum
from typing import Optional
from typing import Tuple

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from app.db import Base


class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, autoincrement=True, primary_key=True)
    player_one = Column(Text, nullable=False)
    player_two = Column(Text, nullable=True)
    player_one_score = Column(Integer, default=0, nullable=False)
    player_two_score = Column(Integer, default=0, nullable=False)


class Move(str, enum.Enum):
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"


class Result(str, enum.Enum):
    WIN = "WIN"
    LOSE = "LOSE"
    TIE = "TIE"


move_db_type = Enum(Move, name="MOVE_ENUM", create_constraint=True)


class Turn(Base):
    __tablename__ = "turn"
    id = Column(Integer, autoincrement=True, primary_key=True)
    player_one_move = Column(move_db_type, nullable=True)
    player_two_move = Column(move_db_type, nullable=True)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship("Game")

    def calc_player_results(self) -> Tuple[Optional[Result], Optional[Result]]:
        if self.player_one_move is None or self.player_two_move is None:
            return None, None
        elif self.player_one_move == self.player_two_move:
            return Result.TIE, Result.TIE
        elif (
            self.player_one_move == Move.ROCK
            and self.player_two_move == Move.SCISSORS
            or self.player_one_move == Move.PAPER
            and self.player_two_move == Move.ROCK
            or self.player_one_move == Move.SCISSORS
            and self.player_two_move == Move.PAPER
        ):
            return Result.WIN, Result.LOSE
        else:
            return Result.LOSE, Result.WIN
