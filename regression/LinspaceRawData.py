class LinspaceRawData:
    def __init__(self, data, timestep = 0.1,start_time = 0.0, end_time = 30.0):
        self.timestep = timestep
        self.start_time = start_time
        self.end_time = end_time
        self.data = data

    