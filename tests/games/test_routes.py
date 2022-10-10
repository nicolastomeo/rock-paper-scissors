from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app import models
from app.games.dependencies import get_games_repository
from app.games.schemas import GameCreate
from app.main import get_application


@pytest.fixture()
def player_one_name():
    return "test_name"


@pytest.fixture()
def game_id():
    return 1


@pytest.fixture()
def mock_games_repository(player_one_name: str, game_id: int):
    mock_games = AsyncMock()
    mock_games.create_game = AsyncMock(
        return_value=models.Game(
            id=game_id,
            player_one=player_one_name,
            player_one_score=0,
            player_two_score=0,
        )
    )
    return mock_games


@pytest.fixture
def api_app(mock_games_repository: AsyncMock):
    app = get_application()
    app.dependency_overrides[get_games_repository] = lambda: mock_games_repository
    return app


async def test_create_game_invalid(api_app: FastAPI):
    invalid_game_data = {"player_two": "name"}
    async with AsyncClient(base_url="http://testserver", app=api_app) as client:
        response = await client.post("/games", json=invalid_game_data)

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_game(
    api_app: FastAPI,
    mock_games_repository: AsyncMock,
    player_one_name: str,
    game_id: int,
):
    valid_game_data = {"player_one": player_one_name}
    async with AsyncClient(base_url="http://testserver", app=api_app) as client:
        response = await client.post("/games", json=valid_game_data)
    assert response.status_code == HTTP_200_OK
    response_json = response.json()
    assert response_json["id"] == game_id
    assert response_json["player_one"] == player_one_name
    assert response_json["player_two"] is None
    assert response_json["player_one_score"] == 0
    assert response_json["player_two_score"] == 0
    mock_games_repository.create_game.assert_called_with(
        GameCreate(player_one=player_one_name, player_two=None)
    )
