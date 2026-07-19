from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field


class OtpRequest(BaseModel):
    identification: int = Field(gt=0, description="Identificación numérica del asociado")
    email: EmailStr


class OtpRequestResponse(BaseModel):
    message: str


class BalanceRequest(BaseModel):
    identification: int = Field(gt=0, description="Identificación numérica del asociado")
    otp: str = Field(pattern=r"^\d{6}$", description="Código OTP de seis dígitos")


class BalanceResponse(BaseModel):
    balance: Decimal
