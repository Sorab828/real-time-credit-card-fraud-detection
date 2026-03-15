from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

transactions = []


# ---------------- RISK CALCULATION ----------------

def calculate_risk(amount, location, category, card, frequency):

    # Amount Risk
    if amount < 2000:
        amount_risk = 20
    elif amount < 5000:
        amount_risk = 40
    elif amount < 10000:
        amount_risk = 70
    else:
        amount_risk = 100


    # Location Risk
    indian_cities = ["Delhi", "Mumbai", "Noida", "Meerut", "Lucknow"]

    if location in indian_cities:
        location_risk = 20
    else:
        location_risk = 100


    # Frequency Risk
    if frequency <= 2:
        frequency_risk = 20
    elif frequency <= 5:
        frequency_risk = 50
    else:
        frequency_risk = 80


    # Category Risk
    category_scores = {
        "Grocery": 20,
        "Shopping": 40,
        "Travel": 70,
        "Electronics": 90
    }

    category_risk = category_scores.get(category, 40)


    # Time Risk
    hour = datetime.now().hour

    if 0 <= hour <= 5:
        time_risk = 80
    else:
        time_risk = 30


    # Card Risk
    card_scores = {
        "RuPay": 20,
        "Visa": 40,
        "MasterCard": 50
    }

    card_risk = card_scores.get(card, 30)


    # ---------------- FORMULA ----------------
    risk_score = (
        (amount_risk * 0.30) +
        (location_risk * 0.20) +
        (frequency_risk * 0.20) +
        (category_risk * 0.15) +
        (time_risk * 0.10) +
        (card_risk * 0.05)
    )

    return round(risk_score, 2)


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/analytics")
def analytics():

    total = len(transactions)

    fraud = len([t for t in transactions if t["status"] == "Fraud"])
    legit = len([t for t in transactions if t["status"] == "Legitimate"])
    suspicious = len([t for t in transactions if t["status"] == "Suspicious"])

    data = {
        "total": total,
        "fraud": fraud,
        "legit": legit,
        "suspicious": suspicious
    }

    return render_template("analytics.html", data=data)

@app.route("/transactions")
def transactions_page():
    return render_template("transactions.html", transactions=transactions)


@app.route("/fraud-alerts")
def fraud_alerts():

    fraud_list = [t for t in transactions if t["status"] == "Fraud"]

    return render_template("alerts.html", frauds=fraud_list)


# ---------------- PROCESS TRANSACTION ----------------

@app.route("/process", methods=["POST"])
def process():

    data = request.json

    amount = float(data["amount"])
    location = data["location"]
    card = data["card"]
    category = data["category"]

    frequency = len(transactions) + 1

    risk = calculate_risk(amount, location, category, card, frequency)


    # Decision Logic
    if risk >= 70:
        status = "Fraud"
    elif risk >= 40:
        status = "Suspicious"
    else:
        status = "Legitimate"


    transaction = {
        "status": status,
        "amount": amount,
        "risk": risk,
        "location": location,
        "card": card,
        "time": datetime.now().strftime("%H:%M:%S")
    }

    transactions.append(transaction)


    fraud_count = len([t for t in transactions if t["status"] == "Fraud"])

    avg_risk = sum([t["risk"] for t in transactions]) / len(transactions)


    return jsonify({
        "transaction": transaction,
        "total": len(transactions),
        "fraud": fraud_count,
        "avg_risk": avg_risk
    })


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)