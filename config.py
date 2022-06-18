import logging

from pydantic import BaseConfig


class Settings(BaseConfig):
    logger_name = 'ac-clip'
    logger = logging.getLogger(logger_name)


settings = Settings()
