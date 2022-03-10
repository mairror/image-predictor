import logging
import sys

from config.settings import LOG_LEVEL


def logger(name: str) -> logging.Logger:
    """
    Generates a logger handler to use in the application.

    :param name: type(str): Name of the logger (avoiding using root logger)
    :return:logging.Logger
    """
    logger = logging.getLogger(name)
    level = logging.getLevelName(LOG_LEVEL)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


image_predictor = logger("image_predictor")
