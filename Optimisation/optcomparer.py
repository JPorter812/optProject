import numpy as np
from scipy.optimize import minimize
from sympy import sympify, symbols, diff
import time

from Optimisation.OptimisationProblem import OptimisationProblem
from .Optimiser import Optimiser
import xmltodict
OPTIMISATION_PROBLEMS = "optimization_problems"

class OptimizationComparer:
    #'newton-cg', 'dogleg' 'trust-ncg', 'trust-exact', 'trust-krylov' to be added.
    methods = ['nelder-mead', 'powell', 'cg', 'bfgs', 'l-bfgs-b', 'tnc', 'cobyla', 'slsqp', 'trust-constr', 'diff_ev',
               "basinhopping", "dual_annealing"]
    def __init__(self, filename):
        self._filename = filename
        self.optimization_problems = self.parse_optimization_problems()
        

    def parse_optimization_problems(self):
        with open(self._filename, 'r') as file:
                optimization_problems_dict = xmltodict.parse(file.read())
        optimisation_problems = []
        for problem_xml in optimization_problems_dict[OPTIMISATION_PROBLEMS]["PROBLEM"]: 
            problem = OptimisationProblem()

            expression = problem["equation"]
            self.objective_function = sympify(expression)
            lower_bounds = problem["lower_bound"]["par"]
            self.bounds



        return optimization_problems

    def solve_optimization_problem(self):
        initial_guess = np.ones(len(self.symbols_list))  # Initial guess
        for method in self.methods:
            start_time = time.time()
            optimiser: Optimiser = Optimiser()
            opts ={}
            bounds = self.optimization_problems["bounds"] 
            options = {"opts": opts, "startguess": initial_guess, "bounds": bounds}
            solution, best_eval, iterations, evaluations = optimiser.optimise(self.evaluate_objective_function_value, optalgo=method, options = options)
            end_time = time.time()
            print(f"Method: {method}, minimum: {best_eval} Optimal solution: ", *{self.symbols_list[i]: solution[i] for i in range(len(solution))}.items(), end="")
            print(f" iterations: {iterations}", end="")
            print(f" evaluations: {evaluations}", end="")
            print(f" time taken: {end_time - start_time}")
    
    def evaluate_objective_function_value(self, params):
        #as long as we are consistent here with which symbol goes with which input parameter, its ok. 
        #need to be careful when we are putting in specific inital first guesses, and limits. 
        values = {symbol: value for symbol, value in zip(self.symbols_list, params)}
        objective_value = float(self.objective_function.subs(values))
        return objective_value

    def run_optimisations(self):
        print("Available optimization problems:")
        for name in self.optimization_problems:
            print(f"- {name}")

        selected_problem = input("Enter the name of the optimization problem to solve: ")
        generator = (problem for problem in self.optimization_problems[OPTIMISATION_PROBLEMS]["PROBLEM"] if problem["name"] == selected_problem)
        problem = next(generator, None)
        if problem:
            expression = problem["equation"]
            self.objective_function = sympify(expression)
            lower_bounds = problem["lower_bound"]["par"]
            self.bounds
            self.symbols_list = list(self.objective_function.free_symbols)
            print(f"Solving optimization problem '{selected_problem}'...")
            self.solve_optimization_problem()
        else:
            print(f"Optimization problem '{selected_problem}' not found.")

def main(): 
    solver = OptimizationComparer('D:\cs50\optProject\optimisation\optimization_problems.xml')
    solver.run_optimisations()

if __name__ == "__main__":
    main()
