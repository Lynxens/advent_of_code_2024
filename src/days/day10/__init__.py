from collections import deque
from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    trail_map: np.ndarray


@advent_info(day=10)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data(read_int_matrix(file_path, sep=''))

    @expected_answers(example_answer=36, answer=841)
    def puzzle_1(self, data: Data) -> int:
        trailheads = np.argwhere(data.trail_map == 0)

        score = 0

        for (row, col) in trailheads:
            queue = deque([(row, col)])
            visited = set()
            reachable_peaks = set()

            while queue:
                row, col = queue.popleft()

                if (row, col) in visited:
                    continue
                else:
                    visited.add((row, col))

                current_height = data.trail_map[row, col]

                if current_height == 9:
                    reachable_peaks.add((row, col))
                    continue

                for (r, c) in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
                    if (
                            (r, c) not in visited and
                            in_2d_grid(data.trail_map, r, c) and
                            data.trail_map[r, c] - current_height == 1
                    ):
                        queue.append((r, c))

            score += len(reachable_peaks)

        return score


    @expected_answers(example_answer=81, answer=1875)
    def puzzle_2(self, data: Data) -> int:
        trailheads = np.argwhere(data.trail_map == 0)

        score = 0

        for (row, col) in trailheads:
            queue = deque([(row, col, set())])
            reachable_peaks = dict()

            while queue:
                row, col, visited = queue.popleft()

                if (row, col) in visited:
                    continue
                else:
                    visited.add((row, col))

                current_height = data.trail_map[row, col]

                if current_height == 9:
                    if (row, col) in reachable_peaks:
                        reachable_peaks[(row, col)] += 1
                    else:
                        reachable_peaks[(row, col)] = 1

                    continue

                for (r, c) in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
                    if (
                            (r, c) not in visited and
                            in_2d_grid(data.trail_map, r, c) and
                            data.trail_map[r, c] - current_height == 1
                    ):
                        queue.append((r, c, visited.copy()))

            score += sum(reachable_peaks.values())

        return score
