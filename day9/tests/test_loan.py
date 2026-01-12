import pytest
from loan.models import Loan


def test_calculate_emi():
    loan = Loan(100000, 10, 1)
    assert loan.calculate_emi() > 0


def test_invalid_inputs():
    with pytest.raises(ValueError):
        Loan(-1, 10, 1)
