from fastapi import HTTPException
from pydantic.main import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


class GameNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Game not found")


class TurnNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Turn not found")


class InvalidTurn(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid turn move.")
