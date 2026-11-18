def validate_customer(name, age):
    if name is None or not name.strip():
        return False

    if age is None or age < 18:
        return False

    return True


def validate_quantity(quantity):
    return quantity is not None and quantity > 0


def validate_status(status):
    valid_statuses = ["Completed", "Pending", "Cancelled"]

    if status is None:
        return False

    return status.strip().capitalize() in valid_statuses


def calculate_order_amount(quantity, price):
    if quantity is None or price is None:
        raise ValueError("Quantity and price are required")

    if quantity <= 0 or price <= 0:
        raise ValueError("Quantity and price must be positive")

    return round(quantity * price, 2)
