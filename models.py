def validate_transaction(data):
    if "amount" not in data or "type" not in data:
        return False, "Amount and type required"

    if data["type"] not in ["income", "expense"]:
        return False, "Invalid type"

    if data["amount"] <= 0:
        return False, "Amount must be positive"

    return True, ""