import csv


def analyze_repayment_csv(filename):
    total_principal = 0
    total_interest = 0
    total_emi = 0

    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_principal += float(row["principal_paid"])
            total_interest += float(row["interest_paid"])
            total_emi += float(row["emi"])

    return {
        "total_principal_paid": round(total_principal, 2),
        "total_interest_paid": round(total_interest, 2),
        "total_amount_paid": round(total_emi, 2),
        "average_interest" : round(total_interest / 48 ,2) # 4 years * 12
    }


# Test analysis
if __name__ == "__main__":
    result = analyze_repayment_csv("repayment_schedule.csv")

    print("Loan Analytics Summary")
    print("---------------------")
    for key, value in result.items():
        print(f"{key.replace('_', ' ').title()}: ₹{value}")
