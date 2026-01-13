from pydantic import BaseModel


class LoanRequest(BaseModel):
    principal: float
    annual_rate: float
    tenure_years: int


class LoanResponse(BaseModel):
    id: int
    principal: float
    annual_rate: float
    tenure_years: int
    emi: float
