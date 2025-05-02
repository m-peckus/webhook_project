#!/usr/bin/env python3

import os
import stripe
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load keys from .env file
load_dotenv()

app = Flask(__name__)

endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    #print(f"Received webhook payload: {payload}")
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        return 'Signature verification failed.', 400
    except Exception as e:
        return f'Webhook error: {str(e)}', 400

    # Handle the event (only verified)
    if event['type'] == 'checkout.session.completed':
        print("Payment completed!")
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(port=5000, debug=True)