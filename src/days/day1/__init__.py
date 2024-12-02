from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    list1: np.ndarray
    list2: np.ndarray


@advent_info(day=1)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        lines = read_lines(file_path)

        columns = np.array([*map(
            lambda line: [*map(int, split_once(line, '   '))],
            lines,
        )]).T

        return Data(
            list1=columns[0],
            list2=columns[1],
        )

    @expected_answers(example_answer=11, answer=2264607)
    def puzzle_1(self, data: Data) -> int:
        return np.abs(np.sort(data.list1) - np.sort(data.list2)).sum()

    @expected_answers(example_answer=31, answer=19457120)
    def puzzle_2(self, data: Data) -> int:
        list1_freq = dict(zip(*np.unique_counts(data.list1)))
        list2_freq = dict(zip(*np.unique_counts(data.list2)))

        return sum([
            possible_id * list1_freq[possible_id] * list2_freq[possible_id]
            for possible_id in np.intersect1d(data.list1, data.list2)
        ])
