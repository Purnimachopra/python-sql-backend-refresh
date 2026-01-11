import pytest
from loan import Loan


def test_emi_calculation():
    loan = Loan(100000, 10, 1)
    emi = loan.calculate_emi()
    assert emi > 0


def test_invalid_principal():
    with pytest.raises(ValueError):
        Loan(-1000, 10, 1)


def test_invalid_rate():
    with pytest.raises(ValueError):
        Loan(100000, -5, 1)


def test_invalid_tenure():
    with pytest.raises(ValueError):
        Loan(100000, 10, 0)
