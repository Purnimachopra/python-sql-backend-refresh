from fastapi import FastAPI, HTTPException
from models import Loan
from schemas import LoanRequest, EmiResponse, LoanSummaryResponse

app = FastAPI(title="Loan Service API", version="1.0")


@app.get("/")
def health():
    return {"status": "Loan Service is running"}


@app.post("/emi", response_model=EmiResponse)
def calculate_emi(request: LoanRequest):
    try:
        loan = Loan(
            request.principal,
            request.annual_rate,
            request.tenure_years
        )
        return {"emi": loan.calculate_emi()}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/summary", response_model=LoanSummaryResponse)
def loan_summary(request: LoanRequest):
    try:
        loan = Loan(
            request.principal,
            request.annual_rate,
            request.tenure_years
        )
        return loan.summary()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
