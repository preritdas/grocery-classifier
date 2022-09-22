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


def alert_use(number, content):
    texts.send_message(
        f"Grocery list used by {number}. Their list... \n{content}"
    )


concats = {}


@app.route('/inbound-sms', methods=["POST"])
def inbound_sms():
    global concats

    inbound_sms_content = request.get_json()
    if type(inbound_sms_content) is not dict:
        return ('', 400)

    if "concat" in inbound_sms_content and inbound_sms_content["concat"] == "true":
        if int(inbound_sms_content["concat-part"]) < int(inbound_sms_content["concat-total"]):
            concats[inbound_sms_content["msisdn"]] = [inbound_sms_content["text"]]
            print("Storing.")
            return '', 204

        # If this is the final concat message
        print("Reading.")
        inbound_sms_content["text"] = ''.join(concats[inbound_sms_content["msisdn"]] + [inbound_sms_content["text"]])
            
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

    alert_use(sender, result)

    print("Concats:", concats)
    return '', 204


if __name__ == '__main__':
    app.run(port=8080, debug=True)
