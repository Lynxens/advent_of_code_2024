from collections import deque
from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    grid: np.ndarray
    is_example: bool


@advent_info(day=20)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data(
            grid=read_str_matrix(file_path),
            is_example='example' in file_path,
        )

    @expected_answers(example_answer=44, answer=1530)
    def puzzle_1(self, data: Data) -> int:
        min_time_save = 1 if data.is_example else 100
        track = follow_track(data.grid)
        track_indices = {coord: idx for idx, coord in enumerate(track)}

        return sum(
            len(find_cheat_options(
                grid=data.grid,
                track=track,
                track_indices=track_indices,
                min_time_save=min_time_save,
                max_steps=2,
                start_index=i,
            ))
            for i in range(len(track))
        )

    @expected_answers(example_answer=285, answer=1033983)
    def puzzle_2(self, data: Data) -> int:
        min_time_save = 50 if data.is_example else 100
        track = follow_track(data.grid)
        track_indices = {coord: idx for idx, coord in enumerate(track)}

        return sum(
            len(find_cheat_options(
                grid=data.grid,
                track=track,
                track_indices=track_indices,
                min_time_save=min_time_save,
                max_steps=20,
                start_index=i,
            ))
            for i in range(len(track))
        )


def follow_track(grid: np.ndarray) -> list[tuple[int, int]]:
    track = []

    start = tuple(map(int, np.argwhere(grid == 'S')[0]))
    end = tuple(map(int, np.argwhere(grid == 'E')[0]))

    (y, x) = start
    while (y, x) != end:
        track.append((y, x))

        for (dy, dx) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ny, nx = y + dy, x + dx

            if grid[ny, nx] != '#' and (ny, nx) not in track:
                y, x = ny, nx
                break

    track.append(end)

    return track


def find_cheat_options(
        grid: np.ndarray,
        track: list[tuple[int, int]],
        track_indices: dict[tuple[int, int], int],
        min_time_save: int,
        max_steps: int,
        start_index: int,
) -> set[tuple[int, int]]:
    cheat_options = set()

    start = track[start_index]
    queue = deque([(start, 0)])
    visited = set()

    while queue:
        pos, steps = queue.popleft()

        if steps > max_steps:
            continue

        if pos in visited:
            continue

        visited.add(pos)

        if pos in track_indices and track_indices[pos] - start_index - steps >= min_time_save:
            cheat_options.add(pos)

        (y, x) = pos
        for (dy, dx) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ny, nx = y + dy, x + dx

            if not in_2d_grid(grid, ny, nx):
                continue

            queue.append(((ny, nx), steps + 1))

    return cheat_options
