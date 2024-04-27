from LinspaceRawData import LinspaceRawData
from Model_runner import Model_runner
import numpy as np
from Optimiser import Optimiser

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
        optimiser: Optimiser = Optimiser() 
        options = {"opts": opts, "startguess": startingguess, "bounds": bounds}
        return optimiser.optimise(self.objective_function, optalgo, options)
