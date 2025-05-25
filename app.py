from flask import Flask, jsonify, request, send_from_directory
import requests
import json

app = Flask(__name__)

PAYU_API_URL = "https://sandbox.api.payulatam.com/payments-api/4.0/service.cgi"
MERCHANT_ID = "1024716"
API_LOGIN = "Q10SI1l819l1Rbl"
API_KEY = "F5XwOiBeHGVJXnmzg5otfjzY7S"

def pay_with_token(token, amount, order_id):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "language": "es",
        "command": "SUBMIT_TRANSACTION",
        "merchant": {
            "apiLogin": API_LOGIN,
            "apiKey": API_KEY
        },
        "transaction": {
            "order": {
                "accountId": MERCHANT_ID,
                "referenceCode": order_id,
                "description": "Pago automático con token",
                "language": "es",
                "notifyUrl": "https://tuweb.com/notify",
                "additionalValues": {
                    "TX_VALUE": {
                        "value": float(amount),
                        "currency": "USD"
                    }
                }
            },
            "payer": {
                "merchantPayerId": "cliente123",
                "paymentMethod": "VISA",
                "paymentCountry": "US",
                "accountNumber": token
            },
            "type": "AUTHORIZATION_AND_CAPTURE",
            "paymentMethod": "VISA",
            "paymentCountry": "US",
            "deviceSessionId": "device_session_123",
            "ipAddress": "127.0.0.1",
            "cookie": "cookie_xyz",
            "userAgent": "Mozilla/5.0"
        },
        "test": True
    }

    response = requests.post(PAYU_API_URL, headers=headers, data=json.dumps(payload))
    return response.json()

@app.route("/pago-automatico", methods=["POST"])
def pago_automatico():
    data = request.json
    token = data.get("token")
    amount = data.get("amount")
    order_id = data.get("order_id")

    if not token or not amount or not order_id:
        return jsonify({"error": "Faltan datos"}), 400

    resultado = pay_with_token(token, amount, order_id)
    return jsonify(resultado)

@app.route("/")
def index():
    return send_from_directory("", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
