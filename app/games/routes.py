from fastapi import APIRouter
from fastapi import Depends
from loguru import logger

from app.exceptions import GameNotFound
from app.games import schemas
from app.games.dependencies import get_games_repository
from app.games.repository import GamesRepository

router = APIRouter(tags=["games"])


@router.post(
    "",
    response_model=schemas.Game,
)
async def create_game(
    game_create: schemas.GameCreate,
    games_repository: GamesRepository = Depends(get_games_repository),
) -> schemas.Game:
    """Starts a game given player one name and optionally player two name
    (otherwise game is against computer)"""
    if game_create.player_two:
        players_log = f"{game_create.player_two} (human)"
    else:
        players_log = "computer"
    logger.info(
        f"Creating game for player one {game_create.player_one} "
        f"and player two {players_log}"
    )
    game = await games_repository.create_game(game_create)
    return game


@router.get(
    "/{game_id}",
    response_model=schemas.Game,
)
async def get_game(
    game_id: int,
    games_repository: GamesRepository = Depends(get_games_repository),
) -> schemas.Game:
    """Fetch a game"""
    logger.info(f"Fetching game {game_id}")
    game = await games_repository.get_game(game_id)
    if game is None:
        raise GameNotFound()
    return game
