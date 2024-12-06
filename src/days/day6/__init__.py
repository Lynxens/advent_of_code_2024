from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    grid: np.ndarray
    grid_size: int
    start_pos: tuple[int, int]

get_next_direction = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N',
}

get_next_pos = {
    'N': lambda r, c: (r - 1, c),
    'E': lambda r, c: (r, c + 1),
    'S': lambda r, c: (r + 1, c),
    'W': lambda r, c: (r, c - 1),
}

class Guard:
    __slots__ = ['pos', 'orientation', 'visited', 'steps']

    def __init__(self, start_pos: tuple[int, int]):
        self.pos = start_pos
        self.orientation = 'N'
        self.visited = set()
        self.steps = []

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
        self.steps.append((*self.pos, self.orientation))
        self.pos = self.forward_pos()

@advent_info(day=6)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        grid = np.array([[*line.rstrip()] for line in read_lines(file_path)])
        [row, col] = np.argwhere(grid == '^')[0]
        grid[row, col] = '.'

        return Data(grid, grid_size=grid.shape[0], start_pos=(int(row), int(col)))

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
        object_positions = [(int(coord[0]), int(coord[1])) for coord in np.argwhere(data.grid == '#')]

        movement_map = dict()
        for (r, c) in object_positions:
            movement_map[(r, c)] = {
                'N': find_next_obstacle((r + 1, c), 'N', data),
                'E': find_next_obstacle((r, c - 1), 'E', data),
                'S': find_next_obstacle((r - 1, c), 'S', data),
                'W': find_next_obstacle((r, c + 1), 'W', data),
            }

        loops_detected = set()
        default_guard = Guard(data.start_pos)
        generate_guard_path(default_guard, height, width, object_positions)
        for (obstacle_row, obstacle_col, orientation) in default_guard.steps[1:]:
            if (obstacle_row, obstacle_col) in loops_detected:
                continue

            obstacle_movement = {
                'N': find_next_obstacle((obstacle_row + 1, obstacle_col), 'N', data),
                'E': find_next_obstacle((obstacle_row, obstacle_col - 1), 'E', data),
                'S': find_next_obstacle((obstacle_row - 1, obstacle_col), 'S', data),
                'W': find_next_obstacle((obstacle_row, obstacle_col + 1), 'W', data),
            }

            current, direction = find_next_obstacle(data.start_pos, 'W', data, (obstacle_row, obstacle_col))
            if current == (obstacle_row, obstacle_col):
                result = obstacle_movement[direction]

                if result is None:
                    continue

                (current, direction) = result

            visited = {(*current, direction)}
            while True:
                result = movement_map[current][direction]

                if result is None:
                    if direction == 'N' and current[0] + 1 == obstacle_row and current[1] < obstacle_col:
                        result = obstacle_movement['E']
                    elif direction == 'E' and current[1] - 1 == obstacle_col and current[0] < obstacle_row:
                        result = obstacle_movement['S']
                    elif direction == 'S' and current[0] - 1 == obstacle_row and current[1] > obstacle_col:
                        result = obstacle_movement['W']
                    elif direction == 'W' and current[1] + 1 == obstacle_col and current[0] > obstacle_row:
                        result = obstacle_movement['N']
                else:
                    (next_pos, next_dir) = result
                    # Detect if intersects with extra obstacle
                    if (
                            (next_dir == 'N' and next_pos[1] == obstacle_col and current[0] > obstacle_row > next_pos[0]) or
                            (next_dir == 'E' and next_pos[0] == obstacle_row and current[1] < obstacle_col < next_pos[1]) or
                            (next_dir == 'S' and next_pos[1] == obstacle_col and current[0] < obstacle_row < next_pos[0]) or
                            (next_dir == 'W' and next_pos[0] == obstacle_row and current[1] > obstacle_col > next_pos[1])
                    ):
                        result = obstacle_movement[next_dir]

                if result is None:
                    break

                (current, direction) = result
                if (*current, direction) in visited:
                    loops_detected.add((obstacle_row, obstacle_col))
                    break

                visited.add((*current, direction))

        return len(loops_detected)

    @expected_answers(example_answer=6, answer=1915)
    def puzzle_2_slow(self, data: Data) -> int:
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


def find_next_obstacle(start: tuple[int, int], direction: str, data: Data, extra_obstacle: tuple[int, int] = None) -> tuple[tuple[int, int], str] | None:
    if not (0 <= start[0] < data.grid_size and 0 <= start[1] < data.grid_size):
        return None

    current = start
    direction = get_next_direction[direction]

    while True:
        next_pos = get_next_pos[direction](*current)

        # Check out of bounds
        if not (0 <= next_pos[0] < data.grid_size and 0 <= next_pos[1] < data.grid_size):
            return None

        if next_pos == extra_obstacle or data.grid[next_pos] == '#':
            return next_pos, direction

        current = next_pos