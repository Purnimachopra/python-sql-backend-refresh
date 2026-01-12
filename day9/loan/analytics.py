def loan_summary(loan):
    emi = loan.calculate_emi()
    months = loan.tenure_years * 12
    total_payment = round(emi * months, 2)

    return {
        "emi": emi,
        "total_payment": total_payment,
        "tenure_months": months
    }
