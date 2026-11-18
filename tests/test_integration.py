from src.data_quality.validators import (
    validate_customer,
    validate_quantity,
    validate_status,
    calculate_order_amount
)


def process_order(order):

    # Validate customer
    if not validate_customer(
        order["customer_name"],
        order["age"]
    ):
        return None

    # Validate quantity
    if not validate_quantity(order["quantity"]):
        return None

    # Validate order status
    if not validate_status(order["status"]):
        return None

    # Calculate order amount
    amount = calculate_order_amount(
        order["quantity"],
        order["price"]
    )

    return {
        "order_id": order["order_id"],
        "customer_name": order["customer_name"],
        "order_amount": amount,
        "status": order["status"]
    }


def test_complete_order_pipeline():

    order = {
        "order_id": 301,
        "customer_name": "John Smith",
        "age": 28,
        "quantity": 2,
        "price": 1000,
        "status": "Completed"
    }

    result = process_order(order)

    assert result is not None
    assert result["order_id"] == 301
    assert result["order_amount"] == 2000


def test_pipeline_rejects_invalid_customer():

    order = {
        "order_id": 302,
        "customer_name": "Robert",
        "age": 17,
        "quantity": 2,
        "price": 1000,
        "status": "Completed"
    }

    assert process_order(order) is None


def test_pipeline_rejects_invalid_quantity():

    order = {
        "order_id": 303,
        "customer_name": "John Smith",
        "age": 28,
        "quantity": -1,
        "price": 1000,
        "status": "Completed"
    }

    assert process_order(order) is None


def test_pipeline_rejects_invalid_status():

    order = {
        "order_id": 304,
        "customer_name": "John Smith",
        "age": 28,
        "quantity": 2,
        "price": 1000,
        "status": "Unknown"
    }

    assert process_order(order) is None
