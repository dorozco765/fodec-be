import hashlib
import hmac
import time


class OtpService:
    """OTP de ventana temporal, verificable por cualquier instancia de Cloud Run."""

    def __init__(self, secret: str, ttl_seconds: int):
        if not secret:
            raise ValueError("OTP_SECRET debe estar configurado")
        self._secret = secret.encode()
        self._ttl_seconds = ttl_seconds

    def create(self, identification: str, email: str) -> str:
        return self._code(identification, email, self._time_window())

    def verify(self, identification: str, email: str, code: str) -> bool:
        current_window = self._time_window()
        for window in (current_window, current_window - 1):
            if hmac.compare_digest(self._code(identification, email, window), code):
                return True
        return False

    def _time_window(self) -> int:
        return int(time.time() // self._ttl_seconds)

    def _code(self, identification: str, email: str, window: int) -> str:
        payload = f"{identification}:{email}:{window}".encode()
        digest = hmac.new(self._secret, payload, hashlib.sha256).digest()
        return f"{int.from_bytes(digest[:8], 'big') % 1_000_000:06d}"
