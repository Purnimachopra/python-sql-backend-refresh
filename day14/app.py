from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import LoanCalculator, LoanRecord
from schemas import LoanRequest, LoanResponse

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
