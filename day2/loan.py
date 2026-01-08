class Loan:
    """
    Represents a Loan for a customer.
    """
    def __init__(self, customer_name, principal, rate, term_years):
        self.customer_name = customer_name
        self.principal = principal
        self.rate = rate
        self.term_years = term_years

    def calculate_simple_interest(self):
        return (self.principal * self.rate * self.term_years) / 100

    def summary(self):
        interest = self.calculate_simple_interest()
        total_payment = self.principal + interest
        return (f"Loan Summary for {self.customer_name}:\n"
                f"Principal: {self.principal}\n"
                f"Rate: {self.rate}%\n"
                f"Term: {self.term_years} years\n"
                f"Simple Interest: {interest}\n"
                f"Total Payment: {total_payment}")


# Test the class
if __name__ == "__main__":
    loan1 = Loan("Purnima Chopra", 100000, 8.5, 2)
    print(loan1.summary())
