class Loan:
    def __init__(self, customer_name, principal, annual_rate, tenure_years):
        if principal <= 0 or annual_rate <= 0 or tenure_years <= 0:
            raise ValueError("Principal, rate, and tenure must be positive values")

        self.customer_name = customer_name
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
        schedule = []

        balance = self.principal
        monthly_rate = self.annual_rate / (12 * 100)
        emi = self.calculate_emi()
        months = self.tenure_years * 12

        for month in range(1, months + 1):
            interest = round(balance * monthly_rate, 2)
            principal_paid = round(emi - interest, 2)
            balance = round(balance - principal_paid, 2)

            schedule.append({
                "month": month,
                "emi": emi,
                "principal_paid": principal_paid,
                "interest_paid": interest,
                "remaining_balance": max(balance, 0)
            })

        return schedule


# Test the schedule
if __name__ == "__main__":
    loan = Loan("Purnima Chopra", 300000, 9.0, 3)
    schedule = loan.repayment_schedule()

    print("First 5 months repayment schedule:\n")
    for row in schedule[:5]:
        print(row)
print("\nLast month:")
print(schedule[-1])