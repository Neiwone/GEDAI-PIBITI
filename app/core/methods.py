from pyDecision.algorithm import ahp_method, bw_method
from app.schemas.weight import CalculateAHPWeights, CalculateBWMWeights
import numpy as np

class BWM():
    # Most Important Criteria
    mic: np.ndarray
    # Least Important Criteria
    lic: np.ndarray

    def __init__(self, mic: list[float], lic: list[float]):
        self.mic = np.array(mic)
        self.lic = np.array(lic)

    def get_weight(self) -> list:
        return list(bw_method(self.mic, self.lic, eps_penalty = 1, verbose = False))



class AHP():
    matrix: np.ndarray

    def __init__(self, matrix: list[list[float]]):
        self.matrix = np.array(matrix)

    def get_weight(self) -> list:
        weights, rc = ahp_method(self.matrix, wd = 'geometric')
        return list(weights)



def calculate_weights(request: CalculateAHPWeights | CalculateBWMWeights) -> list:
    if type(request) == CalculateAHPWeights:
        return AHP(request.matrix).get_weight()
    elif type(request) == CalculateBWMWeights:
        return BWM(request.most_important, request.least_important).get_weight()
    else:
        raise ValueError(f'Unknown request type: {type(request)}')
