import numpy as np


def minmax(a: np.ndarray) -> tuple[int, int]:
    return a.min(), a.max()