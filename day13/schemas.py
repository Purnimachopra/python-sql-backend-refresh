from pydantic import BaseModel
from typing import List


class LoanRequest(BaseModel):
    principal: float
    annual_rate: float
    tenure_years: int


class ScheduleItem(BaseModel):
    month: int
    emi: float
    interest_paid: float
    principal_paid: float
    remaining_balance: float


class RepaymentScheduleResponse(BaseModel):
    schedule: List[ScheduleItem]
