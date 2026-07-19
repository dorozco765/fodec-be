import smtplib
from email.message import EmailMessage


class SmtpEmailSender:
    def __init__(self, host: str | None, port: int, username: str | None, password: str | None, sender: str | None, starttls: bool):
        self.host, self.port = host, port
        self.username, self.password = username, password
        self.sender, self.starttls = sender, starttls

    def send_otp(self, recipient: str, otp: str) -> None:
        if not self.host or not self.sender:
            raise RuntimeError("El envío de correo no está configurado")
        message = EmailMessage()
        message["Subject"] = "Código de acceso FODEC"
        message["From"] = self.sender
        message["To"] = recipient
        message.set_content(f"Tu código de verificación FODEC es: {otp}\n\nNo lo compartas con nadie.")
        with smtplib.SMTP(self.host, self.port, timeout=10) as client:
            if self.starttls:
                client.starttls()
            if self.username and self.password:
                client.login(self.username, self.password)
            client.send_message(message)
