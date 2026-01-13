from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import LoanCalculator, LoanRecord
from schemas import LoanRequest, LoanResponse, LoanListResponse

from typing import List
from fastapi import Query

app = FastAPI(title="Loan Service with Database")

# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/loan", response_model=LoanResponse)
def create_loan(request: LoanRequest, db: Session = Depends(get_db)):
    try:
        calculator = LoanCalculator(
            request.principal,
            request.annual_rate,
            request.tenure_years
        )
        emi = calculator.calculate_emi()

        record = LoanRecord(
            principal=request.principal,
            annual_rate=request.annual_rate,
            tenure_years=request.tenure_years,
            emi=emi
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/loans", response_model=LoanListResponse)
def get_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    loans = db.query(LoanRecord).offset(skip).limit(limit).all()
    return {"loans": loans}

@app.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan_by_id(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(LoanRecord).filter(LoanRecord.id == loan_id).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    return loan