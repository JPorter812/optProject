from xyanfunc import XYanalytical_function

def test_evaluate(): 
    function = XYanalytical_function("x^2 + 5")
    assert function.evaluate_function(x=3) == 14

