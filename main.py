"""
Main.
"""
# External
from flask import Flask, request

# Project
import classification
import texts
import utils


app = Flask(__name__)


@app.route('/inbound-sms', methods=["POST"])
def inbound_sms():
    inbound_sms_content = request.get_json()
    if type(inbound_sms_content) is not dict:
        return ('', 400)

    sender = inbound_sms_content["msisdn"]
    grocery_list = inbound_sms_content["text"]

    texts.send_message(
        content = (result := classification.classify_grocery_list(grocery_list)),
        recipient = sender
    )

    if sender in utils.CUSTOM_RECIPIENTS:
        texts.send_message(
            content = result,
            recipient = utils.CUSTOM_RECIPIENTS[sender]
        )


    return '', 204


if __name__ == '__main__':
    app.run(port=8080)
