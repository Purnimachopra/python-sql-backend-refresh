class Loan:
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

    def repayment_schedule(self):
        emi = self.calculate_emi()
        balance = self.principal
        monthly_rate = self.annual_rate / (12 * 100)
        months = self.tenure_years * 12

        schedule = []

        for month in range(1, months + 1):
            interest = round(balance * monthly_rate, 2)
            principal_paid = round(emi - interest, 2)
            balance = round(balance - principal_paid, 2)

            if balance < 0:
                balance = 0

            schedule.append({
                "month": month,
                "emi": emi,
                "interest_paid": interest,
                "principal_paid": principal_paid,
                "remaining_balance": balance
            })

        return schedule
