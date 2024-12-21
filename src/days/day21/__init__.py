from dataclasses import dataclass
from functools import lru_cache

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    codes: list[str]

Keyboard = {
    'numeric': {
        '7': (0, 0),
        '8': (0, 1),
        '9': (0, 2),
        '4': (1, 0),
        '5': (1, 1),
        '6': (1, 2),
        '1': (2, 0),
        '2': (2, 1),
        '3': (2, 2),
        '0': (3, 1),
        'A': (3, 2),
    },
    'directional': {
        '^': (0, 1),
        'A': (0, 2),
        '<': (1, 0),
        'v': (1, 1),
        '>': (1, 2),
    },
}


@advent_info(day=21)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data(read_lines(file_path))

    @expected_answers(example_answer=126384, answer=212488)
    def puzzle_1(self, data: Data) -> int:
        return sum(
            int(code[:-1]) * shortest_sequence(code, max_depth=2)
            for code in data.codes
        )

    @expected_answers(example_answer=154115708116294, answer=258263972600402)
    def puzzle_2(self, data: Data) -> int:
        return sum(
            int(code[:-1]) * shortest_sequence(code, max_depth=25)
            for code in data.codes
        )

def shortest_sequence(sequence: str, depth: int = 0, max_depth: int = 2) -> int:
    current = (3, 2) if depth == 0 else (0, 2)
    keyboard = Keyboard['numeric' if depth == 0 else 'directional']

    return sum(
        shortest_path(current, current := keyboard[char], depth, max_depth)
        for char in sequence
    )

@lru_cache(maxsize=None)
def shortest_path(start: tuple[int, int], end: tuple[int, int], depth: int, max_depth: int) -> int:
    paths = collect_paths(start, end, avoid_pos=(3, 0) if depth == 0 else (0, 0))

    if depth == max_depth:
        return min(map(len, paths))

    return min(shortest_sequence(path, depth + 1, max_depth) for path in paths)

def collect_paths(current: tuple[int, int], end: tuple[int, int], avoid_pos: tuple[int, int], path: str = '') -> list[str]:
    if current == end:
        return [path + 'A']
    if current == avoid_pos:
        return []

    paths = []
    (y, x), (end_y, end_x) = current, end

    if x < end_x:
        paths += collect_paths((y, x + 1), end, avoid_pos, path + '>')
    if y > end_y:
        paths += collect_paths((y - 1, x), end, avoid_pos, path + '^')
    if y < end_y:
        paths += collect_paths((y + 1, x), end, avoid_pos, path + 'v')
    if x > end_x:
        paths += collect_paths((y, x - 1), end, avoid_pos, path + '<')

    return paths