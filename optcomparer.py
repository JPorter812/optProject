import numpy as np
from scipy.optimize import minimize
from sympy import sympify, symbols, diff
import time
from Optimiser import Optimiser

class OptimizationComparer:
    #'newton-cg', 'dogleg' 'trust-ncg', 'trust-exact', 'trust-krylov' to be added.
    methods = ['nelder-mead', 'powell', 'cg', 'bfgs', 'l-bfgs-b', 'tnc', 'cobyla', 'slsqp', 'trust-constr', 'diff_ev']
    def __init__(self, filename):
        self.optimization_problems = self.parse_optimization_problems(filename)

    def parse_optimization_problems(self, filename):
        optimization_problems = {}
        with open(filename, 'r') as file:
            for line in file:
                name, expression = line.strip().split(':')
                optimization_problems[name.strip()] = expression.strip()
        return optimization_problems

    def solve_optimization_problem(self):
        initial_guess = np.ones(len(self.symbols_list))  # Initial guess
        for method in self.methods:
            start_time = time.time()
            optimiser: Optimiser = Optimiser()
            opts ={}
            bounds = [(0,10)] *len(self.symbols_list)  
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
        if selected_problem in self.optimization_problems:
            expression = self.optimization_problems[selected_problem]
            self.objective_function = sympify(expression)
            self.symbols_list = list(self.objective_function.free_symbols)
            print(f"Solving optimization problem '{selected_problem}'...")
            self.solve_optimization_problem()
        else:
            print(f"Optimization problem '{selected_problem}' not found.")

if __name__ == "__main__":
    solver = OptimizationComparer('D:\cs50\optProject\optimization_problems.txt')
    solver.run_optimisations()
