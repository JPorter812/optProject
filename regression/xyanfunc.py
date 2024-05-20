from sympy import symbols, sympify


class Objective_function:
    def __init__(self, limits):
        self.limits = limits

    def evaluate_function(values):
        pass


class XYanalytical_function(Objective_function):
    def __init__(self, expression_str):
        super().__init__(
            [
                {"variable": "x", "min": 0, "max": 100},
                {"variable": "y", "min": 0, "max": 100},
            ]
        )
        self.x, self.y = symbols("x,y")
        self.expression = sympify(expression_str.lower())

    def evaluate_function(self, **values):
        y = 0 if "y" not in values else values["y"]
        return self.expression.subs({self.x: values["x"], self.y: y})
