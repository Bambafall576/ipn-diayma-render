import os
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.before_request
def log_request():
    logging.info(f"➡️ {request.method} {request.path}")

@app.route("/", methods=["GET"])
def home():
    return "test 6 : IPN SERVER DIAYMA OK", 200

payments = {}

@app.route("/ipn", methods=["POST"])
def ipn():
    logging.info("🔥 IPN REÇUE")
    data = request.json
    logging.info(f"📦 DATA : {data}")
    ###
    try:
        product_list = data["products"][0]   # liste de paires
        product_dict = dict(product_list)    # conversion en dict
        payment_id = product_dict["id"]
    except Exception as e:
        logging.error(f"❌ Mauvais format IPN : {e}")
        return jsonify({"error": "bad format"}), 400

    ###
    """
    try:
        payment_id = data["products"][0][0]["id"]
    except Exception as e:
        logging.error("❌ Mauvais format IPN")
        return jsonify({"error": "bad format"}), 400
    """

    payments[payment_id] = "SUCCESS"
    return jsonify({"status": "ok"}), 200

@app.route("/status/<payment_id>", methods=["GET"])
def status(payment_id):
    return jsonify({
        "payment_id": payment_id,
        "status": payments.get(payment_id, "PENDING")
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)




