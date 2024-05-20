from Model import Model
import warnings
import math


class SimpleExponential(Model):
    def __init__(self, A, B, y0):
        super().__init__(y0)
        self._A = A
        self._B = B

    @property
    def B(self):
        """The B property."""
        return self._B

    @property
    def A(self):
        return self._A

    # forward euler
    def advance(self, timestep):
        with warnings.catch_warnings(record=True) as w:
            dydt = (
                (self.y - self.B) / self.A
                if not math.isclose(self.A, 0, abs_tol=1e-3)
                else 0.0
            )
            self._y = self.y + dydt * timestep
            if any(issubclass(warn.category, RuntimeWarning) for warn in w):
                # Handle the warning
                print("Caught a RuntimeWarning")

        return self.y
