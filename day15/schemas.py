from pydantic import BaseModel
from typing import List


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


class LoanListResponse(BaseModel):
    loans: List[LoanResponse]
