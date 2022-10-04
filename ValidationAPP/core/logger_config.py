from enum import Enum
import logging
from typing import Literal, Optional
from core.config import settings


logger = logging.getLogger()
if settings.REPORT_DEBUG:
    logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class ErrorType(Enum):
    INFO = "Info"
    ERROR = "Error"
    EXCEPTION = "Exception"
    DEBUG = "Debug"


def log_handler(
    message,
    log_type: Literal[ErrorType.INFO, ErrorType.ERROR, ErrorType.EXCEPTION, ErrorType.DEBUG],
    request_payload: Optional[str],
):
    log_message = f"{message} - payload: {request_payload}"
    if log_type == ErrorType.INFO:
        logger.info(log_message)
    elif log_type == ErrorType.ERROR:
        logger.error(log_message)
    elif log_type == ErrorType.EXCEPTION:
        logger.exception(log_message)
    elif log_type == ErrorType.DEBUG:
        logger.debug(log_message)
