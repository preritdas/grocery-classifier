import classification
import utils


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

   
def test_custom_mappings():
   for setup in utils.SETUPS:
      lst = classification._classify_items(GROCERY_LIST_TEST, setup=setup)
      assert lst
      
      # Check the order
      order = utils.SETUPS["Whole Foods"][:] + ["none"]
      order = [key for key in lst.keys() if key in order[:]]
      assert order == list(lst.keys())
