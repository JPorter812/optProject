from Optimisation.optcomparer import OptimizationComparer as oc
import os
import sys

def test_parse_xml():
    print("path: ", sys.path)
    print("hello")
    file_path = os.path.join(__file__, r"..\..\optimization_problems.xml")
    optcomparer: oc = oc(file_path)

    assert optcomparer.optimisation_problems[0].name == "opt1"
