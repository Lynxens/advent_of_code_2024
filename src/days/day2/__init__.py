from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    reports: list[np.ndarray]


@advent_info(day=2)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data(
            reports=[*map(int_array, read_lines(file_path))],
        )

    @expected_answers(example_answer=2, answer=502)
    def puzzle_1(self, data: Data) -> int:
        return sum(is_safe_report(report) for report in data.reports)

    @expected_answers(example_answer=4, answer=544)
    def puzzle_2(self, data: Data) -> int:
        return sum(
            any(
                is_safe_report(np.delete(report, removed_level))
                for removed_level in range(len(report))
            ) for report in data.reports
        )

def is_safe_report(report: np.ndarray) -> bool:
    d_min, d_max = minmax(np.diff(report))

    return 1 <= d_min <= d_max <= 3 or -3 <= d_min <= d_max <= -1
