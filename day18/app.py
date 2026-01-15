from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User, LoanCalculator,LoanRecord
from schemas import LoanRequest, LoanResponse, LoanListResponse, UserCreate,Token
from jose import JWTError, jwt
from typing import List
from fastapi import Query
from auth import get_current_user,get_password_hash,verify_password,create_access_token,require_admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
def create_loan(request: LoanRequest, db: Session = Depends(get_db), user: str = Depends(get_current_user) ):
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

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed, role=user.role or "user")

    db.add(db_user)
    db.commit()
    return {"msg": "User created"}

@app.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(data={"sub": user.username, "role": user.role })  # 👈 IMPORTANT})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/admin/users")
def list_users(
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    users = db.query(User).all()
    return [{"username": u.username, "role": u.role} for u in users]
