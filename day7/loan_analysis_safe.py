import csv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def analyze_repayment_csv(filename):
    total_principal = 0
    total_interest = 0
    total_emi = 0

    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                total_principal += float(row["principal_paid"])
                total_interest += float(row["interest_paid"])
                total_emi += float(row["emi"])

    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        return None

    except KeyError as e:
        logging.error(f"Missing expected column: {e}")
        return None

    except ValueError as e:
        logging.error(f"Invalid data found in CSV: {e}")
        return None

    finally:
        logging.info("CSV processing attempt completed")

    return {
        "total_principal_paid": round(total_principal, 2),
        "total_interest_paid": round(total_interest, 2),
        "total_amount_paid": round(total_emi, 2)
    }


# Test safe analysis
if __name__ == "__main__":
    result = analyze_repayment_csv("repayment_schedule.csv")

    if result:
        logging.info("Loan Analytics Summary")
        for key, value in result.items():
            logging.info(f"{key.replace('_', ' ').title()}: ₹{value}")
