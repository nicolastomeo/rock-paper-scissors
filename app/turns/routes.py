import random

from fastapi import APIRouter
from fastapi import Depends
from loguru import logger

from app.exceptions import GameNotFound
from app.exceptions import HTTPError
from app.exceptions import InvalidTurn
from app.games.dependencies import get_games_repository
from app.games.repository import GamesRepository
from app.models import Move
from app.turns import schemas
from app.turns.dependencies import get_turns_repository
from app.turns.repository import TurnsRepository

router = APIRouter(tags=["turns"])


@router.post("", response_model=schemas.Turn, responses={404: {"model": HTTPError}})
async def create_turn(
    game_id: int,
    turns_repository: TurnsRepository = Depends(get_turns_repository),
) -> schemas.Turn:
    """Starts a turn given an existing game"""
    logger.info(f"Creating turn for game {game_id}")
    turn = await turns_repository.create_turn(game_id)
    return turn


@router.get(
    "/{turn_id}/",
    response_model=schemas.Turn,
    responses={
        404: {"model": HTTPError},
    },
)
async def get_turn(
    game_id: int,
    turn_id: int,
    turns_repository: TurnsRepository = Depends(get_turns_repository),
) -> schemas.TurnResult:
    """Fetches turn given game id and turn id"""
    logger.info(f"Fetching turn {turn_id} for game {game_id}")
    turn = await turns_repository.get_turn(game_id, turn_id)
    return turn


@router.get(
    "/{turn_id}/result",
    response_model=schemas.TurnResult,
    responses={
        404: {"model": HTTPError},
    },
)
async def get_turn_result(
    game_id: int,
    turn_id: int,
    turns_repository: TurnsRepository = Depends(get_turns_repository),
) -> schemas.TurnResult:
    """Fetches and computes turn result given game id and turn id"""
    logger.info(f"Fetching turn {turn_id} for game {game_id}")
    turn = await turns_repository.get_turn(game_id, turn_id)
    player_one_result, player_two_result = turn.calc_player_results()
    return schemas.TurnResult(
        player_one_result=player_one_result, player_two_result=player_two_result
    )


@router.patch(
    "/{turn_id}",
    response_model=schemas.TurnResult,
    responses={
        404: {"model": HTTPError},
        400: {"model": HTTPError},
        409: {"model": HTTPError},
    },
)
async def update_turn(
    game_id: int,
    turn_id: int,
    turn_update: schemas.TurnUpdate,
    games_repository: GamesRepository = Depends(get_games_repository),
    turns_repository: TurnsRepository = Depends(get_turns_repository),
) -> schemas.TurnResult:
    """Play a turn given an existing game, turn and moves from player one or two"""
    logger.info(f"Playing turn {turn_id} for game {game_id}")
    game = await games_repository.get_game(game_id)
    if game is None:
        raise GameNotFound()
    player_one_move = turn_update.player_one_move
    player_two_move = turn_update.player_two_move
    if game.player_two is None:
        if turn_update.player_two_move is not None:
            raise InvalidTurn()
        else:
            # Computer move
            player_two_move = random.choice(list(Move))
    turn = await turns_repository.update_turn(
        game_id, turn_id, player_one_move, player_two_move
    )
    player_one_result, player_two_result = turn.calc_player_results()
    return schemas.TurnResult(
        player_one_result=player_one_result, player_two_result=player_two_result
    )
