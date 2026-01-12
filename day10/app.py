from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Loan

app = FastAPI(title="Loan Calculator API")


class LoanRequest(BaseModel):
    principal: float
    annual_rate: float
    tenure_years: int


@app.get("/")
def health_check():
    return {"status": "Loan API running"}


@app.post("/calculate-emi")
def calculate_emi(request: LoanRequest):
    try:
        loan = Loan(
            request.principal,
            request.annual_rate,
            request.tenure_years
        )
        emi = loan.calculate_emi()
        return {"emi": emi}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
