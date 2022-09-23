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
    concat = False

    if "concat" in inbound_sms_content and inbound_sms_content["concat"] == "true":
        concat = True
        concat_ref = inbound_sms_content["concat-ref"]
        concat_part = int(inbound_sms_content["concat-part"])

        if not sender in payloads:
            payloads[sender] = {
                concat_ref: {
                    concat_part: inbound_sms_content
                }
            }
        elif concat_ref not in payloads[sender]:
            payloads[sender][concat_ref] = {
                concat_part: inbound_sms_content
            }
        else:
            payloads[sender][concat_ref][concat_part] = inbound_sms_content

        required_concats = list(range(1, int(inbound_sms_content["concat-total"]) + 1))
        print(f"{required_concats = }")
        present_concats = list(payloads[sender][concat_ref].keys())
        print(f"{present_concats = }")
        all_present = all(req in present_concats for req in required_concats)
        print(f"{all_present = }")
        
        if not all_present:  # not all messages stored
            print("Outstanding payloads:", payloads)
            return Response(status=204)
        
        # All are present, construct the grocery list
        messages = []
        for n in required_concats: 
            messages.append(payloads[sender][concat_ref][n]["text"])

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
    if concat: del payloads[sender]
    print("Outstanding payloads:", payloads)

    return Response(status=204)


if __name__ == '__main__':
    app.run(port=8080)
