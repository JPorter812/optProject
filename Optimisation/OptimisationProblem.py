from dataclasses import dataclass
from typing import *

@dataclass
class OptimisationProblem:
    bounds:  List[Tuple[float,float]]
    equation: str
    

