from decimal import Decimal

from app.repositories.associate_repository import AssociateRepository, normalize_email
from app.services.email_sender import SmtpEmailSender
from app.services.otp_service import OtpService


GENERIC_OTP_MESSAGE = "Si los datos están registrados, recibirás un código de verificación en el correo indicado."
NOT_FOUND_OTP_MESSAGE = f"{GENERIC_OTP_MESSAGE} [No existe]"


class AssociateService:
    def __init__(
        self,
        repository: AssociateRepository,
        otp_service: OtpService,
        email_sender: SmtpEmailSender,
        development_mode: bool = False,
    ):
        self._repository = repository
        self._otp_service = otp_service
        self._email_sender = email_sender
        self._development_mode = development_mode

    def request_otp(self, identification: int, email: str) -> str:
        associate = self._repository.find_by_identification(identification)
        if associate is None or associate.email != normalize_email(email):
            return NOT_FOUND_OTP_MESSAGE if self._development_mode else GENERIC_OTP_MESSAGE
        self._email_sender.send_otp(associate.email, self._otp_service.create(associate.identification, associate.email))
        return GENERIC_OTP_MESSAGE

    def get_balance(self, identification: int, otp: str) -> Decimal | None:
        associate = self._repository.find_by_identification(identification)
        if associate is None or not self._otp_service.verify(associate.identification, associate.email, otp):
            return None
        return associate.balance
