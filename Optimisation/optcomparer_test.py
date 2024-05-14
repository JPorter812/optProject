from Optimisation.optcomparer import OptimizationComparer as oc

def test_parse_xml(): 
    optcomparer : oc = oc(r'D:\cs50\optProject\optimisation\optimization_problems.xml')

    opt_problems = optcomparer.parse_optimization_problems()

    assert opt_problems["optimization_problems"]["problem"]["name"] == "opt1"

if __name__ == "__main__": 
    test_parse_xml
