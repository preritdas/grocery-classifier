import classification


GROCERY_LIST_TEST = """
3 apples
4 bananas
   3 chicken thighs
1 hair dye
3   bacons
 3 cilantro
1 bread  


"""


def test_classification():
    assert classification.classify_grocery_list(GROCERY_LIST_TEST)
    