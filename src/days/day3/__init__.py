import re
from dataclasses import dataclass
from re import RegexFlag

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    instructions: str


@advent_info(day=3)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data(read_full(file_path))

    @expected_answers(example_answer=(161,161), answer=155955228)
    def puzzle_1(self, data: Data) -> int:
        return sum([a * b for a, b in find_multiplications(data.instructions)])

    @expected_answers(example_answer=(161,48), answer=100189366)
    def puzzle_2(self, data: Data) -> int:
        enabled_sections = []
        start = 0

        for match in re.finditer(r"(?P<do>do\(\))|(?P<dont>don't\(\))", data.instructions, RegexFlag.MULTILINE):
            if match.group('do') and start is None:
                start = match.end()
            elif match.group('dont') and start is not None:
                enabled_sections.append((start, match.start()))
                start = None

        if start is not None:
            enabled_sections.append((start, len(data.instructions)))

        return sum([a * b for a, b in find_multiplications(data.instructions, enabled_sections)])

def find_multiplications(instructions: str, enabled_sections: list[tuple[int, int]] = None) -> list[tuple[int, int]]:
    if enabled_sections is None:
        enabled_sections = [(0, len(instructions))]

    mul_matches = re.finditer(r"mul\((?P<a>\d{1,3}),(?P<b>\d{1,3})\)", instructions, RegexFlag.MULTILINE)

    return [
        (int(match.group('a')), int(match.group('b')))
        for match in mul_matches if pos_in_ranges(match.start(), enabled_sections)
    ]

def pos_in_ranges(pos: int, ranges: list[tuple[int, int]]) -> bool:
    for start, end in ranges:
        if start <= pos <= end:
            return True

    return False
