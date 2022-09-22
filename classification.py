"""
Responsible for turning a list of groceries with quantity into a classified
ordered list.
"""
# External
import translators

# Project
import utils


def _parse_list(grocery_list: str) -> set[tuple[int, str]]:
    """Takes in a list of groceries prefaced with their quantity. Example below.

    3 apples
    1 banana
    2 chicken

    Args:
        grocery_list (str): List of groceries in the format specified above.

    Returns:
        set[tuple[int, str]]: List of tuples with quantity and item name. Plurality
        in the name is preserved.
    """
    assert isinstance(grocery_list, str)

    grocery_list_split = grocery_list.splitlines()
    while '' in grocery_list_split: grocery_list_split.remove('')
    
    items = []
    for item in grocery_list_split:
        split = item.split()

        try: item_tup = int(split[0]), " ".join(split[1:])
        except ValueError: item_tup = "", " ".join(split)

        items.append(tuple(item_tup))

    return set(items)

def _classify(item: str) -> tuple[str, str]:
    """
    Determines the category of item. Returns an empty string if no category
    is matched. Returns a tuple of category and item useful if translated.
    """
    check_item = utils.singularize(item).lower()

    for category in utils.MAPPING:
        if check_item in utils.MAPPING[category]: 
            return category, item

    # No category found, try translation
    for category in utils.MAPPING:
        if (translated := translators.google(item)) in utils.MAPPING[category]:
            return category, translated
    
    return "", item


def _order_classification(classification: dict) -> dict[str, list[tuple[int, str]]]:
    """Reorder categories to match the mapping."""
    for category in classification:
        if category == "none": continue
        classification[category] = sorted(
            classification[category], 
            key = lambda item: utils.MAPPING[category].index(
                utils.singularize(item[1].lower())
            )
        )

    classification_keys = list(classification.keys())
    if "none" in classification_keys: 
        none_present = True
        classification_keys.remove("none")
    else:
        none_present = False

    key_order = sorted(
        classification_keys, 
        key = lambda category: list(utils.MAPPING.keys()).index(category)
    )

    if none_present: 
        key_order.append("none")
    
    return {key: classification[key] for key in key_order}


def _classify_items(grocery_list: str) -> dict[str, list[tuple[int, str]]]:
    """Classify the grocery list."""
    return_classifications = {"none": []}
    for item_tup in (parsed_list := _parse_list(grocery_list)):
        # Update the item if it was translated by _classify
        item_tup = list(item_tup)
        category, item_tup[1] = _classify(item_tup[1])
        item_tup = tuple(item_tup)

        if not category: 
            return_classifications["none"].append(item_tup)
        elif category not in return_classifications:
            return_classifications[category] = [item_tup]
        else:
            return_classifications[category].append(item_tup)

    # return return_classifications
    return _order_classification(return_classifications)


def _format_list(item_list: dict[str, list[tuple[int, str]]]) -> str:
    """Turn the classified list into a string grocery list."""
    return_str = ""
    for category, items in item_list.items():
        if not items: continue
        return_str += f"{category.title()}: \n"

        for pos, item in enumerate(items): 
            return_str += f"- {item[0]} {item[1]}".strip()
            if pos < len(items) - 1: return_str += '\n'

        return_str += "\n\n"
    
    return return_str[:-2]


def classify_grocery_list(grocery_list: str) -> str:
    """Classify the grocery list and return a formatted string grocery list."""
    return _format_list(_classify_items(grocery_list))


if __name__ == '__main__':
    print(classify_grocery_list(
        grocery_list = "12 bananas\n1 Bread\nWhole milk\n1 baby carrots"
    ))