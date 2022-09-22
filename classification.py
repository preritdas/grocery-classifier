"""
Responsible for turning a list of groceries with quantity into a classified
ordered list.
"""
# Internal
import os

# Project
import utils


def _parse_list(grocery_list: str) -> list[tuple[int, str]]:
    """Takes in a list of groceries prefaced with their quantity. Example below.

    3 apples
    1 banana
    2 chicken

    Args:
        grocery_list (str): List of groceries in the format specified above.

    Returns:
        list[tuple[int, str]]: List of tuples with quantity and item name. Plurality
        in the name is preserved.
    """
    assert isinstance(grocery_list, str)
    return [tuple(item.split()) for item in grocery_list.splitlines()]


if __name__ == '__main__':
    print(_parse_list("3    apples\n  1 banana \n 2 chicken\n"))
