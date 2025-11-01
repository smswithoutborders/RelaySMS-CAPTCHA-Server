# SPDX-License-Identifier: GPL-3.0-only

from datetime import datetime
from fastapi import APIRouter, HTTPException
from cachetools import TTLCache
from auth import authenticate_key
from logutils import get_logger
from utils import generate_random_string, get_env_var
from schemas.v1.models import (
    NewCaptchaRequest,
    NewCaptchaResponse,
    SolveCaptchaRequest,
    SolveCaptchaResponse,
    VerifyTokenRequest,
    VerifyTokenResponse,
    CaptchaCacheEntry,
)
from libre_captcha import get_captcha, verify_captcha

logger = get_logger(__name__)

router = APIRouter()

CAPTCHA_CACHE_TTL = int(get_env_var("CAPTCHA_CACHE_TTL", "300"))
CAPTCHA_CACHE_MAX_SIZE = int(get_env_var("CAPTCHA_CACHE_MAX_SIZE", "1000"))

captcha_store = TTLCache(maxsize=CAPTCHA_CACHE_MAX_SIZE, ttl=CAPTCHA_CACHE_TTL)


@router.post("/new", response_model=NewCaptchaResponse)
def request_captcha(req: NewCaptchaRequest):
    """Request a new CAPTCHA challenge."""

    if not authenticate_key(req.client_id):
        logger.error("Invalid Client ID.")
        raise HTTPException(
            status_code=401, detail="Incorrect credentials. Please check and try again."
        )

    captcha_data, _ = get_captcha()
    if not captcha_data:
        raise HTTPException(status_code=503, detail="CAPTCHA service unavailable.")

    challenge_id = generate_random_string(16, "hex")

    cache_entry = CaptchaCacheEntry(
        captcha_id=captcha_data["id"], used=False, created_at=datetime.now()
    )
    captcha_store[challenge_id] = cache_entry

    logger.info("New CAPTCHA challenge created: %s", challenge_id)

    response = {"challenge_id": challenge_id, "image": captcha_data["image"]}
    return NewCaptchaResponse(**response)


@router.post("/solve", response_model=SolveCaptchaResponse)
def solve_captcha(req: SolveCaptchaRequest):
    """Submit a solution for a CAPTCHA challenge."""

    if not authenticate_key(req.client_id):
        logger.error("Invalid Client ID.")
        raise HTTPException(
            status_code=401, detail="Incorrect credentials. Please check and try again."
        )

    if not req.challenge_id:
        raise HTTPException(status_code=400, detail="challenge_id field is required.")

    if not req.answer:
        raise HTTPException(status_code=400, detail="answer field is required.")

    cache_entry = captcha_store.get(req.challenge_id)
    if not cache_entry:
        logger.warning("Challenge ID not found or expired: %s", req.challenge_id)
        raise HTTPException(
            status_code=404, detail="Challenge ID not found or has expired."
        )

    if cache_entry.used:
        logger.warning("Challenge ID already used: %s", req.challenge_id)
        raise HTTPException(status_code=400, detail="Challenge has already been used.")

    cache_entry.used = True
    captcha_store[req.challenge_id] = cache_entry

    success, message = verify_captcha(cache_entry.captcha_id, req.answer)

    if not success:
        logger.error(
            "CAPTCHA verification failed for challenge_id: %s ", req.challenge_id
        )
        return SolveCaptchaResponse(
            success=False,
            message=message,
        )

    verification_token = generate_random_string(32, "hex")

    cache_entry.token = verification_token
    captcha_store[req.challenge_id] = cache_entry

    logger.info("CAPTCHA solved successfully for challenge_id: %s", req.challenge_id)

    return SolveCaptchaResponse(
        success=True,
        message="CAPTCHA solved successfully.",
        token=req.challenge_id + "-" + verification_token,
    )


@router.post("/verify", response_model=VerifyTokenResponse)
def verify_token(req: VerifyTokenRequest):
    """Verify a CAPTCHA token."""

    if not req.client_secret:
        raise HTTPException(status_code=400, detail="client_secret field is required.")
    if not req.token:
        raise HTTPException(status_code=400, detail="token field is required.")

    if not authenticate_key(req.client_secret, "secret"):
        logger.error("Invalid Client Secret.")
        raise HTTPException(
            status_code=401, detail="Incorrect credentials. Please check and try again."
        )

    [challenge_id, token] = req.token.split("-", 1)

    cache_entry = captcha_store.get(challenge_id)
    if not cache_entry:
        logger.warning(
            "Challenge ID not found or expired for verification: %s", challenge_id
        )
        return VerifyTokenResponse(
            success=False,
            message="Challenge ID not found or has expired.",
            verified=False,
        )

    if not cache_entry.used:
        logger.error("Challenge ID not yet solved: %s ", challenge_id)
        return VerifyTokenResponse(
            success=False,
            message="CAPTCHA challenge has not been solved yet.",
        )

    if not cache_entry.token == token:
        logger.error("Invalid token for challenge_id: %s ", challenge_id)
        return VerifyTokenResponse(success=False, message="Invalid token provided.")

    del captcha_store[challenge_id]
    logger.info("Challenge verified successfully: %s", challenge_id)
    return VerifyTokenResponse(success=True, message="Token verified successfully.")
