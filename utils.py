"""
Utils.
"""
import json
import os

from pattern import en as pattern
import nltk; nltk.download('omw-1.4', quiet=True, raise_on_error=True)


# ---- CONSTANTS ---- 

current_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(current_dir, "pluralization_replacements.json")) as f:
    PLURAL_REPLACEMENTS: dict[str, str] = json.load(f)
    SINGULAR_REPLACEMENTS = {val: key for key, val in PLURAL_REPLACEMENTS.items()}

with open(os.path.join(current_dir, "mapping.json")) as f:
    MAPPING: dict[str, list[str]] = json.load(f)


def pluralize(word: str):
    """
    Use the pattern library to smartly and correctly pluralize the word.
    """
    assert isinstance(word, str)
    return pattern.pluralize(word, custom=PLURAL_REPLACEMENTS)


def singularize(word: str):
    """
    Use the pattern library to smartly and correctly pluralize the word.
    """
    assert isinstance(word, str)
    return pattern.singularize(word, SINGULAR_REPLACEMENTS)
 