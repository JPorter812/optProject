import numpy as np
import matplotlib.pyplot as pyplot
from Model_runner import Model_runner
from Model_fitter import Model_fitter
from SimpleExponential import SimpleExponential
from LinspaceRawData import LinspaceRawData

def main():
    timestep = 0.1
    start_time = 0.0
    end_time = 30.0
    parameters = [10,11,12]
    model_runner = Model_runner(SimpleExponential(*parameters), timestep, start_time, end_time)
    modelResult = model_runner.run_model()

    bounds = [(parameter-5, parameter +5) for parameter in parameters]    
    
    
    pyplot.plot(modelResult.timepoints, modelResult.values)

    # Customize the plot
    pyplot.title('Simple Line Plot')
    pyplot.xlabel('X-axis')
    pyplot.ylabel('Y-axis')

    perturbeddata = LinspaceRawData(perturbdata(modelResult.values, 0.05), timestep, start_time, end_time)

    pyplot.plot(modelResult.timepoints, perturbeddata.data)

    # Show the plot
    model_fitter = Model_fitter(lambda parameters: SimpleExponential(A=parameters[0], B=parameters[1], y0 = parameters[2]), perturbeddata)
    # initial_simplex = [[0,0,0], [0,0,1], [0,1,0], [1,0,0]]
    # opts = {'initial_simplex': initial_simplex}
    opts = {}
    fittedparams = model_fitter.FitModel([1,1,1], 'powell', opts =opts, bounds=bounds)
    fittedModel = SimpleExponential(A=fittedparams[0], B=fittedparams[1], y0 = fittedparams[2])
    model_runner_fitted = Model_runner(fittedModel, timestep, start_time, end_time)
    pyplot.plot(modelResult.timepoints, model_runner_fitted.run_model().values)
    print(*fittedparams)
    pyplot.show()

def perturbdata(theoreticaldata, proportional_uncertainty):
    return theoreticaldata + np.random.normal(loc=0, scale = proportional_uncertainty*theoreticaldata, size = len(theoreticaldata))


if __name__ == "__main__":
    main()

