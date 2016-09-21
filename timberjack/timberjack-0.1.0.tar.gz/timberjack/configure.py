import logging
import structlog

from .processors import CensorSensitiveDataProcessor


def configure_structlog():
    structlog.configure(
        logger_factory=structlog.stdlib.LoggerFactory(),
        processors=[
            structlog.processors.JSONRenderer(),
            # Must be the last processor in the list
            CensorSensitiveDataProcessor(),
        ],
    )
