print("Script started")
def calculate_simple_interest(principal, rate, time):
    """
    Calculate simple interest for a loan
    """
    try:
        interest = (principal * rate * time) / 100
        return interest
    except Exception as e:
        return f"Error occurred: {e}"


if __name__ == "__main__":
    principal = 100000
    rate = 8.5
    time = 2

    interest = calculate_simple_interest(principal, rate, time)
    print(f"Simple Interest: {interest}")
