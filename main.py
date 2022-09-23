"""
Main.
"""
# External
from flask import Flask, request, Response

# Project
import classification
import texts
import utils


app = Flask(__name__)


def alert_use(number, content):
    if number == texts.keys.Nexmo.mynumber: return
    texts.send_message(
        f"Grocery list used by {number}. Their list... \n\n{content}"
    )


payloads = {}


@app.route('/', methods=["GET"])
def inb():
    print("Received.")
    return Response(status=204)


@app.route('/inbound-sms', methods=["POST"])
def inbound_sms():
    global payloads

    inbound_sms_content = request.get_json()
    print("\n", inbound_sms_content, sep="")

    if type(inbound_sms_content) is not dict:
        return Response(status=400)

    # Payload handling
    sender = inbound_sms_content["msisdn"]
    if sender in payloads: payloads[sender].append(inbound_sms_content)
    else: payloads[sender] = [inbound_sms_content]

    if "concat" in inbound_sms_content and inbound_sms_content["concat"] == "true":
        required_concats = list(range(1, int(inbound_sms_content["concat-total"]) + 1))
        present_concats = [int(message["concat-part"]) for message in payloads[sender]]
        all_present = present_concats == required_concats
        print(f"{all_present = }")
        
        if not all_present:  # not all messages stored
            return Response(status=204)
        
        # All are present, construct the grocery list
        messages = [message["text"] for message in payloads[sender]]
        inbound_sms_content["text"] = ''.join(messages)
            
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

    # Temporary usage alerts
    alert_use(sender, result)

    # Payload handling
    del payloads[sender]
    print("Payloads:", payloads)

    return Response(status=204)


if __name__ == '__main__':
    app.run(port=8080)
