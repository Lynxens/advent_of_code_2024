from collections import deque
from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    part1_obstacles: list[tuple[int, int]]
    part2_obstacles: list[tuple[int, int]]
    height: int
    width: int
    start: tuple[int, int]
    end: tuple[int, int]


@advent_info(day=18)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        lines = read_lines(file_path)

        obstacles = list()
        for line in lines:
            x, y = map(int, split_once(line, ','))
            obstacles.append((y, x))

        if 'example' in file_path:
            return Data(
                part1_obstacles=obstacles[:12],
                part2_obstacles=obstacles,
                height=7,
                width=7,
                start=(0, 0),
                end=(6, 6),
            )
        else:
            return Data(
                part1_obstacles=obstacles[:1024],
                part2_obstacles=obstacles,
                height=71,
                width=71,
                start=(0, 0),
                end=(70, 70),
            )

    @expected_answers(example_answer=22, answer=290)
    def puzzle_1(self, data: Data) -> int:
        return find_shortest_path_length(
            obstacles=data.part1_obstacles,
            height=data.height,
            width=data.width,
            start=data.start,
            end=data.end,
        )

    @expected_answers(example_answer='6,1', answer='64,54')
    def puzzle_2(self, data: Data) -> str:
        # Binary search
        low, high = 0, len(data.part2_obstacles)
        while low < high:
            mid = (low + high) // 2

            left_is_corrupted = find_shortest_path_length(
                obstacles=data.part2_obstacles[:(mid - 1)],
                height=data.height,
                width=data.width,
                start=data.start,
                end=data.end,
            ) is None

            right_is_corrupted = find_shortest_path_length(
                obstacles=data.part2_obstacles[:mid],
                height=data.height,
                width=data.width,
                start=data.start,
                end=data.end,
            ) is None

            if left_is_corrupted != right_is_corrupted:
                y, x = data.part2_obstacles[mid - 1]
                return f'{x},{y}'

            if left_is_corrupted:
                high = mid
            else:
                low = mid + 1

def find_shortest_path_length(
    obstacles: list[tuple[int, int]],
    height: int,
    width: int,
    start: tuple[int, int],
    end: tuple[int, int],
) -> int | None:
    queue = deque([(start, [])])
    visited = set()

    while queue:
        (y, x), path = queue.popleft()

        if (y, x) == end:
            return len(path)

        if (y, x) in visited:
            continue

        visited.add((y, x))

        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_y, new_x = y + dy, x + dx

            if (new_y, new_x) in visited:
                continue

            if (new_y, new_x) in obstacles:
                continue

            if not (0 <= new_y < height and 0 <= new_x < width):
                continue

            queue.append(((new_y, new_x), [*path, (y, x)]))

    return None
