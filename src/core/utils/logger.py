import logging
import sys


def create_logger(app_name: str) -> logging.Logger:
    """Настройка основных параметров системы логирования."""
    stream_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(
        handlers=[stream_handler],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    return logging.getLogger(app_name)
