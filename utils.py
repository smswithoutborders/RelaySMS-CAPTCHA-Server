# SPDX-License-Identifier: GPL-3.0-only

import os
import base64
from typing import Optional
from dotenv import load_dotenv
from logutils import get_logger

load_dotenv()
logger = get_logger(__name__)


def get_env_var(key: str, default_value: Optional[str] = None, strict: bool = False):
    """Retrieves the value of a configuration from the environment variables."""
    try:
        value = os.environ[key] if strict else os.getenv(key) or default_value
        if strict and (value is None or value.strip() == ""):
            raise ValueError(f"Configuration '{key}' is missing or empty.")
        return value
    except KeyError as error:
        logger.error(
            "Configuration '%s' not found in environment variables: %s", key, error
        )
        raise
    except ValueError as error:
        logger.error("Configuration '%s' is empty: %s", key, error)
        raise


def generate_random_string(length: int = 16, encoding: str = "hex") -> str:
    """Generates a random string of specified length and encoding."""
    random_bytes = os.urandom(length)
    if encoding == "hex":
        return random_bytes.hex()

    if encoding == "base64":
        return base64.b64encode(random_bytes).decode("utf-8")

    raise ValueError(f"Unsupported encoding: {encoding}")
