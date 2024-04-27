from LinspaceRawData import LinspaceRawData
from Model_runner import Model_runner
from scipy.optimize import minimize
import scipy.optimize
import numpy as np

class Model_fitter: 
    def __init__(self, model_factory, rawdata) -> None:
        self.model_factory = model_factory
        self.rawdata = rawdata

    def calculate_least_squares_error(self, prediction): 
        return 1/len(self.rawdata.data) * np.sum((self.rawdata.data - prediction.values)**2)
        
    def objective_function(self, parameters):
        model = self.model_factory(parameters)
        model_runner = Model_runner(model, self.rawdata.timestep, self.rawdata.start_time, self.rawdata.end_time)
        result = model_runner.run_model()
        return self.calculate_least_squares_error(result)

    def FitModel(self, startingguess, optalgo, bounds = None, opts = None): 
        if optalgo in ['nelder-mead', 'powell', 'cg', 'bfgs', 'l-bfgs-b', 'tnc', 'cobyla', 'slsqp', 'trust-constr']: 
            optresult = minimize(self.objective_function, startingguess, method = optalgo, options=opts, bounds=bounds)
        else: 
            match optalgo: 
                case "diff_ev": 
                    scipy.optimize.differential_evolution(self.objective_function, bounds=bounds)
        return optresult.x
