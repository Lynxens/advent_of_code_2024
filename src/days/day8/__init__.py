from dataclasses import dataclass
from itertools import combinations

import numpy as np

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    grid: np.ndarray
    antenna_pairs: list[tuple[tuple[int, int], tuple[int, int]]]


@advent_info(day=8)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        grid = read_str_matrix(file_path)

        antenna_pairs = []
        for antenna_type in np.unique(grid[grid != '.'].flatten()):
            antenna_coords = np.argwhere(grid == antenna_type)

            for [y1, x1], [y2, x2] in combinations(antenna_coords, r=2):
                antenna_pairs.append((
                    (y1, x1),
                    (y2, x2),
                ))

        return Data(grid, antenna_pairs)

    @expected_answers(example_answer=14, answer=323)
    def puzzle_1(self, data: Data) -> int:
        antinodes = set()

        for [y1, x1], [y2, x2] in data.antenna_pairs:
            dy = y2 - y1
            dx = x2 - x1

            for y, x in [
                (y1 + dy, x1 + dx) if (y1 + dy, x1 + dx) != (y2, x2) else (y2 + dy, x2 + dx),
                (y1 - dy, x1 - dx) if (y1 - dy, x1 - dx) != (y2, x2) else (y2 - dy, x2 - dx),
            ]:
                if in_2d_grid(data.grid, y, x):
                    antinodes.add((y, x))

        return len(antinodes)

    @expected_answers(example_answer=34, answer=1077)
    def puzzle_2(self, data: Data) -> int:
        antinodes = set()

        for [y1, x1], [y2, x2] in data.antenna_pairs:
            antinodes.add((y1, x1))
            antinodes.add((y2, x2))

            dy = y2 - y1
            dx = x2 - x1

            ya, xa = (y1 + dy, x1 + dx) if (y1 + dy, x1 + dx) != (y2, x2) else (y2 + dy, x2 + dx)
            yb, xb = (y1 - dy, x1 - dx) if (y1 - dy, x1 - dx) != (y2, x2) else (y2 - dy, x2 - dx)

            while in_2d_grid(data.grid, ya, xa):
                antinodes.add((ya, xa))
                ya += dy
                xa += dx

            while in_2d_grid(data.grid, yb, xb):
                antinodes.add((yb, xb))
                yb -= dy
                xb -= dx

        return len(antinodes)
