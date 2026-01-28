from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

payments = {}  # transaction_id -> dict(status, amount)

#payments = {}  # transaction_id → status

@app.route("/cancel", methods=["GET"])
def cancel():
    transaction_id = request.args.get("transaction_id")

    if transaction_id:
        payments[transaction_id] = {
            "status": "FAILED"
        }
        print(f"❌ Paiement {transaction_id} annulé")

    return "Paiement annulé", 200

@app.route("/ipn", methods=["POST"])
def ipn():
    data = request.json
    try:
        # products est une liste de listes de paires [clé, valeur]
        product_list = data["products"][0]   
        product_dict = dict(product_list)     
        transaction_id = product_dict["id"]
        amount = int(product_dict["price"])
    except Exception as e:
        logging.error("❌ Mauvais format IPN")
        return jsonify({"error": "bad format"}), 400

    payments[transaction_id] = {"status": "SUCCESS", "amount": amount}
    logging.info(f"✅ Paiement {transaction_id} enregistré avec succès")
    return jsonify({"status": "ok"}), 200

@app.route("/status/<transaction_id>", methods=["GET"])
def status(transaction_id):
    if transaction_id in payments:
        return payments[transaction_id], 200
    return {"status": "PAIEMENT EN COURS"}, 200#return {"status": "PENDING"}, 200

"""
@app.route("/status/<transaction_id>", methods=["GET"])
def status(transaction_id):
    info = payments.get(transaction_id)
    if not info:
        return jsonify({"status": "PENDING"}), 200
    return jsonify(info), 200
"""
@app.route("/", methods=["GET"])
def home():
    return "IPN Server Render OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


