from sqlalchemy import Column, Integer, Float, String
from database import Base


class LoanRecord(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    principal = Column(Float, nullable=False)
    annual_rate = Column(Float, nullable=False)
    tenure_years = Column(Integer, nullable=False)
    emi = Column(Float, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # 👈 NEW

class LoanCalculator:
    def __init__(self, principal, annual_rate, tenure_years):
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if annual_rate <= 0:
            raise ValueError("Rate must be positive")
        if tenure_years <= 0:
            raise ValueError("Tenure must be positive")

        self.principal = principal
        self.annual_rate = annual_rate
        self.tenure_years = tenure_years

    def calculate_emi(self):
        monthly_rate = self.annual_rate / (12 * 100)
        months = self.tenure_years * 12

        emi = (
            self.principal
            * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )
        return round(emi, 2)
    