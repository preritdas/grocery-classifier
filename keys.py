"""
Parse keys into their appropriate types.
"""
import os
import configparser


current_dir = os.path.dirname(os.path.realpath(__file__))
keys_path = os.path.join(current_dir, "keys.ini")

keys = configparser.RawConfigParser()
keys.read(keys_path)


class Nexmo:
    _nexmo_keys = keys["Nexmo"]
    api_key = _nexmo_keys["api_key"]
    api_secret = _nexmo_keys["api_secret"]
    sender = _nexmo_keys["sender"]
    mynumber = _nexmo_keys["receiver"]
