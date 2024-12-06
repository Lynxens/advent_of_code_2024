from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    grid: np.ndarray
    start_pos: tuple[int, int]


class Guard:
    __slots__ = ['pos', 'orientation', 'visited', 'steps']

    def __init__(self, start_pos: tuple[int, int]):
        self.pos = start_pos
        self.orientation = 'N'
        self.visited = set()
        self.steps = set()

    def forward_pos(self) -> tuple[int, int]:
        return {
            'N': lambda r, c: (r - 1, c),
            'E': lambda r, c: (r, c + 1),
            'S': lambda r, c: (r + 1, c),
            'W': lambda r, c: (r, c - 1),
        }[self.orientation](*self.pos)

    def turn_right(self):
        self.orientation = {
            'N': 'E',
            'E': 'S',
            'S': 'W',
            'W': 'N',
        }[self.orientation]

    def move_forward(self):
        self.visited.add(self.pos)
        self.steps.add((*self.pos, self.orientation))
        self.pos = self.forward_pos()

@advent_info(day=6)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        grid = np.array([[*line.rstrip()] for line in read_lines(file_path)])
        [row, col] = np.argwhere(grid == '^')[0]

        return Data(grid, start_pos=(row, col))

    @expected_answers(example_answer=41, answer=5199)
    def puzzle_1(self, data: Data) -> int:
        [height, width] = data.grid.shape
        object_positions = [(coord[0], coord[1]) for coord in np.argwhere(data.grid == '#')]

        guard = Guard(data.start_pos)
        generate_guard_path(guard, height, width, object_positions)

        return len(guard.visited)

    @expected_answers(example_answer=6, answer=1915)
    def puzzle_2(self, data: Data) -> int:
        [height, width] = data.grid.shape
        object_positions = [(coord[0], coord[1]) for coord in np.argwhere(data.grid == '#')]

        default_guard = Guard(data.start_pos)
        generate_guard_path(default_guard, height, width, object_positions)

        not_looping_options = set()
        looping_options = set()
        for i, (row, col, orientation) in enumerate(default_guard.steps, start=1):
            print(f"{i}/{len(default_guard.steps)}")

            forward_pos = {
                'N': lambda r, c: (r - 1, c),
                'E': lambda r, c: (r, c + 1),
                'S': lambda r, c: (r + 1, c),
                'W': lambda r, c: (r, c - 1),
            }[orientation](row, col)

            if forward_pos in looping_options or forward_pos in not_looping_options:
                continue

            guard = Guard(data.start_pos)
            if not generate_guard_path(guard, height, width, [*object_positions, forward_pos]):
                looping_options.add(forward_pos)
            else:
                not_looping_options.add(forward_pos)

        return len(looping_options)

def generate_guard_path(
        guard: Guard,
        height: int,
        width: int,
        object_positions: list[tuple[int, int]],
) -> bool:
    while 0 <= guard.pos[0] < height and 0 <= guard.pos[1] < width:
        while guard.forward_pos() in object_positions:
            guard.turn_right()

        # Check for loop
        if (*guard.pos, guard.orientation) in guard.steps:
            return False

        guard.move_forward()

    return True
