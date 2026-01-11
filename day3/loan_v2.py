class Loan:
    """
    Loan class with validation and EMI calculation
    """

    def __init__(self, customer_name, principal, annual_rate, tenure_years):
        if principal <= 0:
            raise ValueError("Principal must be greater than 0")

        if annual_rate <= 0:
            raise ValueError("Interest rate must be greater than 0")

        if tenure_years <= 0:
            raise ValueError("Tenure must be greater than 0")

        self.customer_name = customer_name
        self.principal = principal
        self.annual_rate = annual_rate
        self.tenure_years = tenure_years
        print("class initiated")

    def calculate_emi(self):
        """
        EMI formula:
        EMI = P * r * (1+r)^n / ((1+r)^n - 1)
        """
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
        total_payment = emi * self.tenure_years * 12

        return f"""
Loan Summary
------------
Customer Name : {self.customer_name}
Principal     : ₹{self.principal}
Interest Rate : {self.annual_rate}%
Tenure        : {self.tenure_years} years
Monthly EMI   : ₹{emi}
Total Payment : ₹{round(total_payment, 2)}
"""


# Test the class
if __name__ == "__main__":
    loan = Loan("Purnima Chopra", -1000, 9.5, 5)
    print(loan.summary())
