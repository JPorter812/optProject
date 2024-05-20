from dataclasses import dataclass
from typing import *


@dataclass
class OptimisationProblem:
    name: str
    bounds: List[Tuple[float, float]]
    equation: str
    initial_guess: List[float]
