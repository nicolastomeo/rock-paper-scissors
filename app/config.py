import logging
from functools import lru_cache

from loguru import logger
from pydantic import BaseSettings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class Settings(BaseSettings):
    """
    Configuration of app
    """

    db_connection: str
    db_debug: bool = False
    logging_level: int = logging.INFO

    class Config:
        env_file = ".env"

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        # Use loguru for uvicorn logs
        loggers = (
            logging.getLogger(name)
            for name in logging.root.manager.loggerDict
            if name.startswith("uvicorn")
        )
        for uvicorn_logger in loggers:
            uvicorn_logger.handlers = []
        logging_logger = logging.getLogger("uvicorn.access")
        logging_logger.handlers = [InterceptHandler(level=self.logging_level)]
        if self.db_debug:
            logging_logger = logging.getLogger("sqlalchemy.engine.Engine")
            logging_logger.handlers.clear()


@lru_cache()
def get_settings():
    return Settings()
