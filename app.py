from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

model = joblib.load("model/fraud_model.pkl")
feature_means = joblib.load("model/feature_means.pkl")

transactions = []

@app.route("/")
def home():
    return render_template("index.html", transactions=transactions)

@app.route("/predict", methods=["POST"])
def predict():

    amount = float(request.form["amount"])
    time = float(request.form["time"])

    # create full feature vector
    features = feature_means.copy()
    features["Time"] = time
    features["Amount"] = amount

    features = features.values.reshape(1, -1)

    # ML probability
    probability = model.predict_proba(features)[0][1]

    # risk calculation (ML + amount factor)
    ml_risk = probability * 100
    amount_risk = (amount / 10000) * 100

    risk = round((ml_risk * 0.7) + (amount_risk * 0.3), 2)
    risk = min(risk, 100)

    # three level classification
    if risk < 30:
        result = "Normal"
    elif risk < 70:
        result = "Suspicious"
    else:
        result = "Fraud"

    transactions.append({
        "time": time,
        "amount": amount,
        "risk": risk,
        "result": result
    })

    return render_template(
        "index.html",
        result=result,
        risk=risk,
        normal=100-risk,
        fraud=risk,
        transactions=transactions
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)