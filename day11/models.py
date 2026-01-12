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

    def summary(self):
        emi = self.calculate_emi()
        months = self.tenure_years * 12
        total_payment = round(emi * months, 2)

        return {
            "principal": self.principal,
            "annual_rate": self.annual_rate,
            "tenure_years": self.tenure_years,
            "emi": emi,
            "total_payment": total_payment
        }
