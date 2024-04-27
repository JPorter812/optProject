from scipy.optimize import minimize
import scipy.optimize

#optimiser for use of comparing optimisation methods. 
class Optimiser: 
    def optimise(self, objective_function, optalgo: str, options: dict): 
        if optalgo in ['nelder-mead', 'powell', 'cg', 'bfgs', 'l-bfgs-b', 'tnc', 'cobyla', 'slsqp', 'trust-constr']: 
            optresult = minimize(objective_function, options["startguess"], method = optalgo, options=options["opts"], bounds=options.get("bounds"))
            
        else: 
            match optalgo: 
                case "diff_ev": 
                    optresult = scipy.optimize.differential_evolution(objective_function, bounds=options.get("bounds"))
                case _: 
                    raise ValueError("Algo method not recognized")
                
        iterations = None
        evaluations = None
        solution = optresult.x
        best_eval= optresult.fun
        if "nit" in optresult.keys():
            iterations = optresult.nit
        if "nfev" in optresult.keys(): 
            evaluations = optresult.nfev
        return solution, best_eval, iterations, evaluations