#!/usr/bin/env python3

import os
import stripe
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv

# Load keys from .env file
load_dotenv()

app = Flask(__name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
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
        abort(400, "Invalid signature")
    

    # Handle the event (only verified)
    if event['type'] == 'payment_intent.succeeded':
        print("Payment succeeded!")

    return jsonify(success=True)

