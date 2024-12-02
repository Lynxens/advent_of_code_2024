from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    data: list[str]


@advent_info(day=None)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data(read_lines(file_path))

    @expected_answers(example_answer=None, answer=None)
    def puzzle_1(self, data: Data) -> int:
        pass

    @expected_answers(example_answer=None, answer=None)
    def puzzle_2(self, data: Data) -> int:
        pass
