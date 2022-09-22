"""
Main.
"""
# External
from flask import Flask, request

# Project
import classification
import texts


app = Flask(__name__)


@app.route('/inbound-sms', methods=["POST"])
def inbound_sms():
    inbound_sms_content = request.get_json()
    if type(inbound_sms_content) is not dict:
        return ('', 400)

    sender = inbound_sms_content["msisdm"]
    grocery_list = inbound_sms_content["text"]

    texts.send_message(
        content = classification.classify_grocery_list(grocery_list),
        recipient = sender
    )
