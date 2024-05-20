import os
import numpy as np
from sympy import sympify
import time

from .OptimisationProblem import OptimisationProblem
from .Optimiser import Optimiser
import xmltodict

OPTIMISATION_PROBLEMS = "optimization_problems"


class OptimizationComparer:
    #'newton-cg', 'dogleg' 'trust-ncg', 'trust-exact', 'trust-krylov' to be added.
    methods = [
        "nelder-mead",
        "powell",
        "cg",
        "bfgs",
        "l-bfgs-b",
        "tnc",
        "cobyla",
        "slsqp",
        "trust-constr",
        "diff_ev",
        "basinhopping",
        "dual_annealing",
    ]

    def __init__(self, filename):
        self._filename = filename
        self.parse_optimization_problems()

    def parse_optimization_problems(self):
        with open(self._filename, "r") as file:
            optimization_problems_dict = xmltodict.parse(file.read())
        self.optimisation_problems = []
        for problem_xml in optimization_problems_dict[OPTIMISATION_PROBLEMS]["problem"]:
            lower_bounds = problem_xml["lower_bound"]["par"]
            upper_bounds = problem_xml["upper_bound"]["par"]
            bounds = [
                (float(lower), float(upper))
                for lower, upper in zip(lower_bounds, upper_bounds)
            ]
            self.optimisation_problems.append(
                OptimisationProblem(
                    name=problem_xml["name"],
                    equation=problem_xml["equation"],
                    initial_guess=[
                        float(value) for value in problem_xml["initial_guess"]["par"]
                    ],
                    bounds=bounds,
                )
            )

    def solve_optimization_problem(self):
        initial_guess = np.ones(len(self.symbols_list))  # Initial guess
        for method in self.methods:
            start_time = time.time()
            optimiser: Optimiser = Optimiser()
            opts = {}
            options = {"opts": opts, "startguess": initial_guess, "bounds": self.bounds}
            solution, best_eval, iterations, evaluations = optimiser.optimise(
                self.evaluate_objective_function_value, optalgo=method, options=options
            )
            end_time = time.time()
            print(
                f"Method: {method}, minimum: {best_eval} Optimal solution: ",
                *{
                    self.symbols_list[i]: solution[i] for i in range(len(solution))
                }.items(),
                end="",
            )
            print(f" iterations: {iterations}", end="")
            print(f" evaluations: {evaluations}", end="")
            print(f" time taken: {end_time - start_time}")

    def evaluate_objective_function_value(self, params):
        # as long as we are consistent here with which symbol goes with which input parameter, its ok.
        # need to be careful when we are putting in specific inital first guesses, and limits.
        values = {symbol: value for symbol, value in zip(self.symbols_list, params)}
        objective_value = float(self.objective_function.subs(values))
        return objective_value

    def run_optimisations(self):
        print("Available optimization problems:")
        for name in self.optimization_problems:
            print(f"- {name}")

        selected_problem = input(
            "Enter the name of the optimization problem to solve: "
        )
        generator = (
            problem
            for problem in self.optimisation_problems
            if problem["name"] == selected_problem
        )
        problem: OptimisationProblem = next(generator, None)
        if problem:
            self.objective_function = sympify(problem.equation)
            self.bounds = problem.bounds
            self.symbols_list = list(self.objective_function.free_symbols)
            print(f"Solving optimization problem '{selected_problem}'...")
            self.solve_optimization_problem()
        else:
            print(f"Optimization problem '{selected_problem}' not found.")
