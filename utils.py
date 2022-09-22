"""
Utils.
"""
from pattern import en as pattern
import nltk; nltk.download('omw-1.4', quiet=True, raise_on_error=True)


def pluralize(word: str):
    """
    Use the pattern library to smartly and correctly pluralize the word.
    """
    assert isinstance(word, str)
    return pattern.pluralize(word)


def singularize(word: str):
    """
    Use the pattern library to smartly and correctly pluralize the word.
    """
    assert isinstance(word, str)
    return pattern.singularize(word)
 