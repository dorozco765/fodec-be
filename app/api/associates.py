from functools import lru_cache

from fastapi import APIRouter, HTTPException, status

from app.config.settings import Settings
from app.repositories.associate_repository import GoogleSheetsAssociateRepository
from app.schemas.associate import BalanceRequest, BalanceResponse, OtpRequest, OtpRequestResponse
from app.services.associate_service import AssociateService
from app.services.email_sender import SmtpEmailSender
from app.services.otp_service import OtpService


router = APIRouter(prefix="/api/associates", tags=["associates"])


@lru_cache
def get_associate_service() -> AssociateService:
    settings = Settings.from_environment()
    return AssociateService(
        repository=GoogleSheetsAssociateRepository(settings.google_sheet_id, settings.google_sheet_range),
        otp_service=OtpService(settings.otp_secret, settings.otp_ttl_seconds),
        email_sender=SmtpEmailSender(
            settings.smtp_host, settings.smtp_port, settings.smtp_username,
            settings.smtp_password, settings.smtp_from, settings.smtp_starttls,
        ),
        development_mode=settings.development_mode,
    )


@router.post("/otp", response_model=OtpRequestResponse, status_code=status.HTTP_202_ACCEPTED)
def request_otp(payload: OtpRequest) -> OtpRequestResponse:
    message = get_associate_service().request_otp(payload.identification, str(payload.email))
    return OtpRequestResponse(message=message)


@router.post("/balance", response_model=BalanceResponse)
def get_balance(payload: BalanceRequest) -> BalanceResponse:
    balance = get_associate_service().get_balance(payload.identification, payload.otp)
    if balance is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP inválido")
    return BalanceResponse(balance=balance)
