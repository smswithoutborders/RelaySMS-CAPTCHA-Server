# SPDX-License-Identifier: GPL-3.0-only

from datetime import datetime
from pydantic import BaseModel


class CaptchaCacheEntry(BaseModel):
    """Cache entry for storing CAPTCHA challenge data."""

    captcha_id: str
    used: bool = False
    verified: bool = False
    token: str = None
    created_at: datetime


class NewCaptchaRequest(BaseModel):
    """Request a new CAPTCHA challenge."""

    client_id: str


class NewCaptchaResponse(BaseModel):
    """Response for a new CAPTCHA challenge."""

    challenge_id: str
    image: str  # Base64-encoded image


class SolveCaptchaRequest(BaseModel):
    """Request to solve a CAPTCHA challenge."""

    client_id: str
    challenge_id: str
    answer: str


class SolveCaptchaResponse(BaseModel):
    """Response for solving a CAPTCHA challenge."""

    success: bool
    message: str
    token: str = None


class VerifyTokenRequest(BaseModel):
    """Request to verify a CAPTCHA token."""

    client_secret: str
    token: str


class VerifyTokenResponse(BaseModel):
    """Response for verifying a CAPTCHA token."""

    success: bool
    message: str


class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str
