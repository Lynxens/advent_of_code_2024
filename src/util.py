from dataclasses import dataclass
from typing import Iterable, Any

import numpy as np


def implode(a: Iterable, sep: str = '') -> str:
    return sep.join(map(str, a))


def minmax(a: np.ndarray) -> tuple[int, int]:
    return a.min(), a.max()


@dataclass(slots=True, frozen=True)
class MooreNeighbourhood:
    NW: Any
    N: Any
    NE: Any
    W: Any
    C: Any
    E: Any
    SW: Any
    S: Any
    SE: Any


def moore_neighbourhood(m: np.ndarray, i: int, j: int) -> MooreNeighbourhood:
    return MooreNeighbourhood(
        NW=m[i - 1, j - 1] if i > 0 and j > 0 else None,
        N=m[i - 1, j] if i > 0 else None,
        NE=m[i - 1, j + 1] if i > 0 and j < m.shape[1] - 1 else None,
        W=m[i, j - 1] if j > 0 else None,
        C=m[i, j] if j < m.shape[1] - 1 else None,
        E=m[i, j + 1] if j < m.shape[1] - 1 else None,
        SW=m[i + 1, j - 1] if i < m.shape[0] - 1 and j > 0 else None,
        S=m[i + 1, j] if i < m.shape[0] - 1 else None,
        SE=m[i + 1, j + 1] if i < m.shape[0] - 1 and j < m.shape[1] - 1 else None,
    )


def in_2d_grid(m: np.ndarray, y: int, x: int) -> bool:
    return 0 <= y < m.shape[0] and 0 <= x < m.shape[1]
