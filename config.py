import logging

from pydantic import BaseConfig


class Settings(BaseConfig):
    logger_name = 'ac-clip'
    logger = logging.getLogger(logger_name)

    service_alive_retry_count_limit = 30


settings = Settings()
