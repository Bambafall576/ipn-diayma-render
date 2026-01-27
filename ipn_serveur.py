#test 2
from flask import Flask, request, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)

IPN_TOKEN = "SECRET_IPN_DIAYMA"
payments = {}

@app.route("/", methods=["GET"])
def home():
    return "IPN SERVER DIAYMA OK - test 2", 200


@app.route("/ipn", methods=["POST"])
def ipn():
    data = request.json
    print("\n🔔 IPN REÇUE 🔔")
    print(json.dumps(data, indent=2))

    if data.get("token") != IPN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    # 🔎 extraction robuste du transaction_id
    transaction_id = None
    products = data.get("products")

    if isinstance(products, list) and len(products) > 0:
        first = products[0]

        if isinstance(first, dict):
            transaction_id = first.get("id")
        elif isinstance(first, list):
            for item in first:
                if isinstance(item, dict) and "id" in item:
                    transaction_id = item["id"]
                    break

    if not transaction_id:
        print("❌ transaction_id introuvable")
        return jsonify({"error": "transaction_id missing"}), 400

    payments[transaction_id] = {
        "status": "SUCCESS",
        "amount": data.get("total"),
        "currency": data.get("devise"),
        "received_at": datetime.utcnow().isoformat()
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

