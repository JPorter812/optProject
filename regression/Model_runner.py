from Model_result import Model_result


import numpy as np


class Model_runner:
    def __init__(self, model, timestep, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.model = model
        self.timestep = timestep

    def run_model(self):
        number_of_timepoints = (
            round((self.end_time - self.start_time) / self.timestep) + 1
        )
        timepoints = np.linspace(self.start_time, self.end_time, number_of_timepoints)
        result = np.zeros(number_of_timepoints)
        result[0] = self.model.y0
        for i in range(1, number_of_timepoints):
            result[i] = self.model.advance(self.timestep)
        return Model_result(timepoints, result)
