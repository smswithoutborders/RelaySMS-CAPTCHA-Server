# SPDX-License-Identifier: GPL-3.0-only

import os
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
numeric_level = getattr(logging, LOG_LEVEL, None)

if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {LOG_LEVEL}")

logging.basicConfig(
    level=numeric_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retrieves a logger instance configured with the specified name.

    Args:
        name (str, optional): The name of the logger. If None, the root logger is
            returned.

    Returns:
        logging.logger: A configured logger instance.
    """
    return logging.getLogger(name)
