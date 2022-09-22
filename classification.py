"""
Responsible for turning a list of groceries with quantity into a classified
ordered list.
"""
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
    return set([tuple(item.split()) for item in grocery_list.splitlines()])


def _classify(item: str) -> str:
    """
    Determines the category of item. Returns an empty string if no category
    is matched.
    """
    item = utils.singularize(item)

    for category in utils.MAPPING:
        if item in utils.MAPPING[category]: 
            return category
    
    return ""


def _order_classification(classification: dict) -> dict[str, list[tuple[int, str]]]:
    """Reorder categories to match the mapping."""
    for category in classification:
        if category == "none": continue
        classification[category] = sorted(
            classification[category], 
            key = lambda item: utils.MAPPING[category].index(utils.singularize(item[1]))
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
        category = _classify(item_tup[1])
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
            return_str += f"{item[0]} {item[1]}"
            if pos < len(items) - 1: return_str += '\n'

        return_str += "\n\n"
    
    return return_str[:-2]


def classify_grocery_list(grocery_list: str) -> str:
    """Classify the grocery list and return a formatted string grocery list."""
    return _format_list(_classify_items(grocery_list))
