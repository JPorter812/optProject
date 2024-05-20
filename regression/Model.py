class Model:

    # y = A(dy/dt) + B
    # y= (y0 - B)*e^(t/A) + B

    def __init__(self, y0):
        self._y0 = y0
        self._y = y0

    @property
    def y0(self):
        """The foo property."""
        return self._y0

    @property
    def y(self):
        """The y property."""
        return self._y

    def advance(timestep):
        pass
