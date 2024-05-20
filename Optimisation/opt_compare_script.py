import os
from Optimisation.optcomparer import OptimizationComparer


def main():
    solver = OptimizationComparer(
        os.path.join(__file__, "..\optimization_problems.xml")
    )
    solver.run_optimisations()


if __name__ == "__main__":
    main()
