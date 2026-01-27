from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

payments = {}  # transaction_id -> dict(status, amount)

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
    info = payments.get(transaction_id)
    if not info:
        return jsonify({"status": "PENDING"}), 200
    return jsonify(info), 200

@app.route("/", methods=["GET"])
def home():
    return "IPN Server Render OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
