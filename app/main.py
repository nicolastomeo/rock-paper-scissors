from fastapi import FastAPI

from app.config import get_settings
from app.games.routes import router as games_router
from app.turns.routes import router as turns_router


def get_application() -> FastAPI:
    settings = get_settings()
    settings.configure_logging()
    app = FastAPI()
    app.include_router(games_router, prefix="/games")
    app.include_router(turns_router, prefix="/games/{game_id}/turns")
    return app


app = get_application()
