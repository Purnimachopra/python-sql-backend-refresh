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

class UserCreate(BaseModel):
    username: str
    password: str
    role: str | None = "user"   # optional

class UserOut(BaseModel):
    username: str
    role: str
    
class Token(BaseModel):
    access_token: str
    token_type: str