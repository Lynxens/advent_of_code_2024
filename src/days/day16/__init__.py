from sys import maxsize
from collections import deque
from dataclasses import dataclass

import numpy as np

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    grid: np.ndarray

STEP_IN_DIRECTION = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1),
}

OPPOSITE_DIRECTION = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E',
}

TURN_DIRECTIONS = {
    'N': ['E', 'W'],
    'E': ['N', 'S'],
    'S': ['W', 'E'],
    'W': ['S', 'N'],
}

@advent_info(day=16)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data(read_str_matrix(file_path))

    @expected_answers(example_answer=(7036, 11048), answer=99460)
    def puzzle_1(self, data: Data) -> int:
        return [*find_paths(data.grid)][-1][0]

    @expected_answers(example_answer=(45, 64), answer=500)
    def puzzle_2(self, data: Data) -> int:
        min_cost = maxsize
        min_visited = set()

        for cost, visited in find_paths(data.grid):
            if cost < min_cost:
                min_cost = cost
                min_visited = visited
            elif cost == min_cost:
                min_visited |= visited

        return len(min_visited)

def find_paths(grid: np.ndarray) -> tuple[int, set[tuple[int, int]]]:
    start = tuple(np.argwhere(grid == 'S')[0])
    queue = deque([(start, 'E', 0, set())])
    min_cost_pos = dict()

    while queue:
        (y, x), direction, cost, visited = queue.popleft()

        for d in [direction, *TURN_DIRECTIONS[direction]]:
            dy, dx = STEP_IN_DIRECTION[d]
            new_pos = (y + dy, x + dx)
            new_cost = cost + (1 if d == direction else 1001)

            if new_pos in visited:
                continue

            if grid[new_pos] == '.':
                if d == direction:  # Only if able to continue in same direction
                    if (y, x) in min_cost_pos and cost > min_cost_pos[(y, x)]:
                        continue
                    else:
                        min_cost_pos[(y, x)] = cost

                queue.append((new_pos, d, new_cost, {*visited, (y, x)}))

            if grid[new_pos] == 'E':
                yield new_cost, {*visited, (y, x), new_pos}