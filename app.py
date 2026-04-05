from flask import Flask, request, jsonify
from database import get_connection, init_db
from models import validate_transaction
from ml import spending_analysis
from utils import check_permission, apply_filters

app = Flask(__name__)
init_db()

# ---------- CREATE ----------
@app.route("/transactions", methods=["POST"])
def create():
    role = request.args.get("role", "viewer")

    if not check_permission(role, "create"):
        return {"error": "Unauthorized"}, 403

    data = request.json
    valid, msg = validate_transaction(data)

    if not valid:
        return {"error": msg}, 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (amount, type, category, date, note) VALUES (?, ?, ?, ?, ?)",
        (data["amount"], data["type"], data.get("category"), data.get("date"), data.get("note"))
    )

    conn.commit()
    conn.close()

    return {"message": "Transaction created"}, 201

# ---------- READ ----------
@app.route("/transactions", methods=["GET"])
def read():
    role = request.args.get("role", "viewer")

    if not check_permission(role, "read"):
        return {"error": "Unauthorized"}, 403

    category = request.args.get("category")
    type_filter = request.args.get("type")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")

    data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    data = apply_filters(data, category, type_filter)

    return jsonify(data)

# ---------- UPDATE ----------
@app.route("/transactions/<int:id>", methods=["PUT"])
def update(id):
    role = request.args.get("role", "viewer")

    if not check_permission(role, "update"):
        return {"error": "Unauthorized"}, 403

    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE transactions SET amount=?, type=?, category=?, date=?, note=? WHERE id=?",
        (data["amount"], data["type"], data.get("category"), data.get("date"), data.get("note"), id)
    )

    conn.commit()
    conn.close()

    return {"message": "Updated"}

# ---------- DELETE ----------
@app.route("/transactions/<int:id>", methods=["DELETE"])
def delete(id):
    role = request.args.get("role", "viewer")

    if not check_permission(role, "delete"):
        return {"error": "Unauthorized"}, 403

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return {"message": "Deleted"}

# ---------- SUMMARY ----------
@app.route("/summary", methods=["GET"])
def summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")

    data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    income = sum(t["amount"] for t in data if t["type"] == "income")
    expense = sum(t["amount"] for t in data if t["type"] == "expense")

    return {
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense,
        "ml_insight": spending_analysis(data)
    }

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)