from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    towels: list[str]
    patterns: list[str]


@advent_info(day=19)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        towels, patterns = split_once(read_full(file_path), '\n\n')

        return Data(
            towels=towels.split(', '),
            patterns=patterns.split('\n'),
        )

    @expected_answers(example_answer=6, answer=280)
    def puzzle_1(self, data: Data) -> int:
        impossible_patterns = set()

        def is_possible_pattern(pattern: str) -> bool:
            if pattern == '':
                return True

            if pattern in impossible_patterns:
                return False

            for towel in data.towels:
                if pattern.startswith(towel) and is_possible_pattern(pattern[len(towel):]):
                    return True

            impossible_patterns.add(pattern)
            return False

        return sum(is_possible_pattern(p) for p in data.patterns)

    @expected_answers(example_answer=16, answer=606411968721181)
    def puzzle_2(self, data: Data) -> int:
        pattern_arrangement_count = dict()

        def count_arrangements(pattern: str) -> int:
            if pattern == '':
                return 1

            if pattern not in pattern_arrangement_count:
                pattern_arrangement_count[pattern] = sum(
                    count_arrangements(pattern[len(towel):])
                    for towel in data.towels
                    if pattern.startswith(towel)
                )

            return pattern_arrangement_count[pattern]

        return sum(count_arrangements(p) for p in data.patterns)
