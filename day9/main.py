from loan.models import Loan
from loan.analytics import loan_summary

if __name__ == "__main__":
    loan = Loan(300000, 9.0, 3)
    summary = loan_summary(loan)

    print("Loan Summary")
    print("------------")
    for key, value in summary.items():
        print(f"{key}: {value}")
