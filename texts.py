"""
Send texts with Nexmo.
"""
# External
import nexmo

# Internal
import os

# Project
import keys


nexmo_client = nexmo.Client(key=keys.Nexmo.api_key, secret = keys.Nexmo.api_secret)
sms = nexmo.Sms(nexmo_client)


def send_message(content: str, recipient: str = keys.Nexmo.mynumber) -> None:
    """Send me a text message."""
    sms.send_message(
        {
            "from": keys.Nexmo.sender,
            "to": recipient,
            "text": str(content)
        }
    )
