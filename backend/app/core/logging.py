from __future__ import annotations

import logging
import logging.config
from typing import Any

import structlog


def configure_logging(level: int | str = logging.INFO) -> None:
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {
                    "format": "%(message)s",
                }
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "plain",
                }
            },
            "loggers": {
                "uvicorn.error": {"handlers": ["default"], "level": level},
                "uvicorn.access": {"handlers": ["default"], "level": level},
                "": {"handlers": ["default"], "level": level},
            },
        }
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            timestamper,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
