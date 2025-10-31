# SPDX-License-Identifier: GPL-3.0-only

from utils import get_env_var
from logutils import get_logger

logger = get_logger(__name__)

CLIENT_ID = get_env_var("CLIENT_ID", strict=True)
CLIENT_SECRET = get_env_var("CLIENT_SECRET", strict=True)


def authenticate_key(key: str, hint: str = "id") -> bool:
    """
    Aithenticate client_id or client_secret keys.

    Args:
        key (str): The key to authenticate.
        hint (str): Hint of key to be authenticated. Either
            'id' or 'secret'. (default='id').

    Return:
        bool: True if valid False ootherwise.
    """
    if hint == "id":
        return key == CLIENT_ID

    if hint == "secret":
        return key == CLIENT_SECRET

    logger.error("Invalid hint %s. Expect 'id' or 'secret'", hint)
    raise ValueError(f"Invalid hint {hint}")
