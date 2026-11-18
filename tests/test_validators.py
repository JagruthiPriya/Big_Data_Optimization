import pytest

from src.data_quality.validators import (
    validate_customer,
    validate_quantity,
    validate_status,
    calculate_order_amount
)


def test_valid_customer():
    assert validate_customer("John", 28) is True


def test_customer_under_18():
    assert validate_customer("Robert", 17) is False


def test_missing_customer_name():
    assert validate_customer("", 25) is False


def test_valid_quantity():
    assert validate_quantity(2) is True


def test_invalid_quantity():
    assert validate_quantity(-1) is False


def test_zero_quantity():
    assert validate_quantity(0) is False


def test_valid_status():
    assert validate_status("Completed") is True


def test_invalid_status():
    assert validate_status("Unknown") is False


def test_order_amount():
    assert calculate_order_amount(2, 100) == 200


def test_invalid_order_amount():
    with pytest.raises(ValueError):
        calculate_order_amount(-1, 100)
