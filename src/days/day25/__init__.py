from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    locks: np.ndarray
    keys: np.ndarray


@advent_info(day=25)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        locks = []
        keys = []

        for grid in read_full(file_path).split('\n\n'):
            lock_or_key = (str_to_str_matrix(grid) == '#').astype(np.int8)
            (locks if lock_or_key[0, 0] else keys).append(lock_or_key)

        return Data(np.array(locks), np.array(keys))

    @expected_answers(example_answer=3, answer=3114)
    def puzzle_1(self, data: Data) -> int:
        # - Lay each key over each lock by addition
        # - Take the max of the 2D grid for each combination
        # - Count the ones without overlap by summing the combinations where the max is 1
        return np.sum(np.max(data.locks[:, None] + data.keys, axis=(2, 3)) == 1)

    @expected_answers(example_answer=None, answer=None)
    def puzzle_2(self, data: Data) -> int:
        pass
