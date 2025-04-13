import numpy as np

def get_best_solution(result):
    if result.X is None:
        raise ValueError("Pas de solutions")
    if len(result.X.shape) == 1:
        return result.X, result.F
    else:
        best_idx = np.argmin(result.F)
        return result.X[best_idx], result.F[best_idx]
