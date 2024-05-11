from loguru import logger
import sys

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
    "<level>{level}</level> "
    "{message}"
)

logger.add(sys.stderr, format=logger_format)
logger.remove(0)
