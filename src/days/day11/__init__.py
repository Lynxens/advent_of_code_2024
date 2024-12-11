from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    stones: list[int]


@advent_info(day=11)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data([*map(int, read_full(file_path).split(' '))])

    @expected_answers(example_answer=55312, answer=231278)
    def puzzle_1(self, data: Data) -> int:
        stone_counts = perform_blinks(initial_stones=data.stones, blinks=25)
        return sum(stone_counts.values())

    @expected_answers(example_answer=65601038650482, answer=274229228071551)
    def puzzle_2(self, data: Data) -> int:
        stone_counts = perform_blinks(initial_stones=data.stones, blinks=75)
        return sum(stone_counts.values())


def perform_blinks(initial_stones: list[int], blinks: int) -> dict[int, int]:
    stone_counts = defaultdict(int, [(stone_id, 1) for stone_id in initial_stones])

    for _ in range(blinks):
        new_stone_counts = defaultdict(int)

        for stone_id, stone_count in stone_counts.items():
            left, right = transform_stone(stone_id)

            new_stone_counts[left] += stone_count

            if right is not None:
                new_stone_counts[right] += stone_count

        stone_counts = new_stone_counts

    return stone_counts


@lru_cache(maxsize=None)
def transform_stone(stone_id: int) -> tuple[int, int | None]:
    if stone_id == 0:
        return 1, None

    stone_id_str = str(stone_id)
    id_length = len(stone_id_str)

    if id_length % 2 == 0:
        half = id_length // 2
        return int(stone_id_str[:half]), int(stone_id_str[half:])

    return stone_id * 2024, None
