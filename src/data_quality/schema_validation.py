import json
from jsonschema import validate, ValidationError

# Load expected schema
with open(
    "schemas/customer_schema.json",
    "r"
) as file:
    schema = json.load(file)

# Valid customer record
valid_customer = {
    "customer_id": 101,
    "customer_name": "John Smith",
    "age": 28,
    "city": "Hyderabad",
    "email": "john@gmail.com"
}

# Simulated schema drift:
# age has changed from integer to string
drift_customer = {
    "customer_id": 102,
    "customer_name": "Jane Wilson",
    "age": "Thirty Two",
    "city": "Bangalore",
    "email": "jane@gmail.com"
}


def check_schema(record, record_name):

    try:
        validate(instance=record, schema=schema)

        print(f"{record_name}: SCHEMA VALID")
        return "PASS"

    except ValidationError as error:

        print(f"{record_name}: SCHEMA DRIFT DETECTED")
        print("Reason:", error.message)

        return "FAIL"


print("Starting Schema Validation")

valid_result = check_schema(
    valid_customer,
    "Valid customer"
)

drift_result = check_schema(
    drift_customer,
    "Drift customer"
)

# Save results
report = {
    "valid_customer": valid_result,
    "drift_customer": drift_result
}

with open(
    "reports/schema_validation/schema_report.json",
    "w"
) as file:

    json.dump(report, file, indent=4)

print("\nSchema validation report saved")
print("Schema Validation Completed")
