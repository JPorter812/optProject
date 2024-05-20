from scipy.optimize import minimize
import scipy.optimize
from pyswarm import pso


class Optimiser_configuration:
    iterations = 5
    swarmsize = 5


# optimiser for use of comparing optimisation methods.
class Optimiser:
    def __init__(self, optimiser_configuration: Optimiser_configuration):
        self._optimiser_configuration = optimiser_configuration

    def optimise(self, objective_function, optalgo: str, options: dict):

        iterations = None
        evaluations = None
        options["opts"]["maxiter"] = self._optimiser_configuration.iterations
        if optalgo in [
            "nelder-mead",
            "powell",
            "cg",
            "bfgs",
            "l-bfgs-b",
            "tnc",
            "cobyla",
            "slsqp",
            "trust-constr",
        ]:
            optresult = minimize(
                objective_function,
                options["startguess"],
                method=optalgo,
                options=options["opts"],
                bounds=options.get("bounds"),
            )

        else:
            match optalgo:
                case "diff_ev":
                    optresult = scipy.optimize.differential_evolution(
                        objective_function,
                        bounds=options.get("bounds"),
                        maxiter=self._optimiser_configuration.iterations,
                    )
                case "basinhopping":
                    optresult = scipy.optimize.basinhopping(
                        objective_function,
                        x0=options.get("startguess"),
                        niter=self._optimiser_configuration.iterations,
                    )
                case "dual_annealing":
                    optresult = scipy.optimize.dual_annealing(
                        objective_function,
                        bounds=options.get("bounds"),
                        maxiter=self._optimiser_configuration.iterations,
                    )
                case "pso":
                    boundslist = options.get("bounds")
                    solution, best_eval = pso(
                        func=objective_function,
                        lb=[bound[0] for bound in boundslist],
                        up=[bound[1] for bound in boundslist],
                        maxiter=self._optimiser_configuration.iterations,
                        swarmsize=self._optimiser_configuration.swarmsize,
                    )

                case _:
                    raise ValueError("Algo method not recognized")

        if optresult:
            solution = optresult.x
            best_eval = optresult.fun
            if "nit" in optresult.keys():
                iterations = optresult.nit
            if "nfev" in optresult.keys():
                evaluations = optresult.nfev
        return solution, best_eval, iterations, evaluations
