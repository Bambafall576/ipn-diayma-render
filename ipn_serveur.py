from flask import Flask, request, jsonify
import logging
import json
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Avant chaque requête, log
@app.before_request
def log_request():
    logging.info(f"➡️ {request.method} {request.path}")

# Route de test
@app.route("/", methods=["GET"])
def home():
    return "IPN SERVER DIAYMA OK", 200

# Fichier où on stocke le statut des paiements
PAYMENT_FILE = "payment_status.json"

# Charger le fichier existant ou créer un dict vide
if os.path.exists(PAYMENT_FILE):
    with open(PAYMENT_FILE, "r") as f:
        payments = json.load(f)
else:
    payments = {}

# Fonction pour sauvegarder les paiements dans le fichier
def save_payments():
    with open(PAYMENT_FILE, "w") as f:
        json.dump(payments, f)

# Route IPN
@app.route("/ipn", methods=["POST"])
def ipn():
    logging.info("🔥 IPN REÇUE")
    data = request.json
    logging.info(f"📦 DATA : {data}")

    try:
        # Convertir la liste de paires en dict pour le produit
        product_list = data["products"][0]  # liste de paires
        product_dict = dict(product_list)
        payment_id = product_dict["id"]
        amount = int(product_dict["price"])
    except Exception as e:
        logging.error(f"❌ Mauvais format IPN : {e}")
        return jsonify({"error": "bad format"}), 400

    # Sauvegarde du paiement
    payments[payment_id] = {
        "status": "SUCCESS",
        "amount": amount
    }
    save_payments()
    logging.info(f"✅ Paiement {payment_id} enregistré avec succès")

    return jsonify({"status": "ok"}), 200

# Route pour récupérer le statut d'un paiement
@app.route("/status/<payment_id>", methods=["GET"])
def status(payment_id):
    payment = payments.get(payment_id)
    if payment:
        return jsonify({
            "payment_id": payment_id,
            "status": payment["status"],
            "amount": payment["amount"]
        })
    else:
        return jsonify({
            "payment_id": payment_id,
            "status": "PENDING",
            "amount": 0
        })

if __name__ == "__main__":
    # Port par défaut 10000 pour Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
