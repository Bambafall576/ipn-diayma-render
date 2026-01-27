from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

IPN_TOKEN = "SECRET_IPN_DIAYMA"

payments = {}

@app.route("/", methods=["GET"])
def home():
    return "IPN SERVER DIAYMA OK", 200


@app.route("/ipn", methods=["POST"])
def ipn():
    data = request.json
    print("\n🔔 IPN REÇUE 🔔")
    print(data)

    if data.get("token") != IPN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    transaction_id = data["products"][0]["id"]

    payments[transaction_id] = {
        "status": "SUCCESS",
        "amount": data.get("total"),
        "currency": data.get("devise"),
        "received_at": datetime.now().isoformat()
    }

    print(f"✅ Paiement confirmé : {transaction_id}")
    return jsonify({"status": "ok"}), 200


@app.route("/status/<transaction_id>", methods=["GET"])
def status(transaction_id):
    if transaction_id not in payments:
        return jsonify({"status": "PENDING"}), 200

    return jsonify(payments[transaction_id]), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
