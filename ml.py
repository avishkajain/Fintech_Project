def spending_analysis(transactions):
    expenses = [t["amount"] for t in transactions if t["type"] == "expense"]

    if not expenses:
        return "No expense data"

    avg = sum(expenses) / len(expenses)

    if avg > 3000:
        return "High average spending pattern detected"
    elif avg > 1000:
        return "Moderate spending pattern"
    else:
        return "Low spending pattern"