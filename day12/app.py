from fastapi import FastAPI, HTTPException
from models import Loan
from schemas import LoanRequest, RepaymentScheduleResponse

app = FastAPI(title="Loan Repayment API", version="1.0")


@app.get("/")
def health():
    return {"status": "Loan Repayment API running"}


@app.post("/repayment-schedule", response_model=RepaymentScheduleResponse)
def repayment_schedule(request: LoanRequest):
    try:
        loan = Loan(
            request.principal,
            request.annual_rate,
            request.tenure_years
        )
        schedule = loan.repayment_schedule()
        return {"schedule": schedule}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
