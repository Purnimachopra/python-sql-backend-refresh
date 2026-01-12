from pydantic import BaseModel


class LoanRequest(BaseModel):
    principal: float
    annual_rate: float
    tenure_years: int


class EmiResponse(BaseModel):
    emi: float


class LoanSummaryResponse(BaseModel):
    principal: float
    annual_rate: float
    tenure_years: int
    emi: float
    total_payment: float
