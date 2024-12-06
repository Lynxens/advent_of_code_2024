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

        # Make map of movements to the next object for each incoming direction to an object
        movement_map = dict()
        for (r, c) in object_positions:
            movement_map[(r, c)] = generate_movement_map(data, r, c)

        # Generate the path that the guard walks without extra object
        default_guard = Guard(data.start_pos)
        generate_guard_path(default_guard, height, width, object_positions)

        loop_detected = set()
        no_loop_detected = set()

        for (obstacle_row, obstacle_col, _) in default_guard.steps[1:]:
            if (obstacle_row, obstacle_col) in loop_detected or (obstacle_row, obstacle_col) in no_loop_detected:
                continue

            obstacle_movement = generate_movement_map(data, obstacle_row, obstacle_col)

            current, direction = find_next_obstacle(data.start_pos, 'W', data, (obstacle_row, obstacle_col))

            # Handle if the path intersects with the extra obstacle
            if current == (obstacle_row, obstacle_col):
                result = obstacle_movement[direction]

                # Result is None if there are no more obstacles in the way
                if result is None:
                    continue

                (current, direction) = result

            visited = {(current, direction)}

            while True:
                result = movement_map[current][direction]

                # Result is None if there are no more obstacles in the way
                if result is None:
                    # Handle if the path intersects with the extra obstacle
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

                    # Handle if the path intersects with the extra obstacle
                    if (
                            (next_dir == 'N' and next_pos[1] == obstacle_col and current[0] > obstacle_row > next_pos[0]) or
                            (next_dir == 'E' and next_pos[0] == obstacle_row and current[1] < obstacle_col < next_pos[1]) or
                            (next_dir == 'S' and next_pos[1] == obstacle_col and current[0] < obstacle_row < next_pos[0]) or
                            (next_dir == 'W' and next_pos[0] == obstacle_row and current[1] > obstacle_col > next_pos[1])
                    ):
                        result = obstacle_movement[next_dir]

                if result is None:
                    no_loop_detected.add((obstacle_row, obstacle_col))
                    break

                (current, direction) = result
                if (current, direction) in visited:
                    loop_detected.add((obstacle_row, obstacle_col))
                    break

                visited.add((current, direction))

        return len(loop_detected)


def generate_guard_path(
        guard: Guard,
        height: int,
        width: int,
        object_positions: list[tuple[int, int]],
):
    while 0 <= guard.pos[0] < height and 0 <= guard.pos[1] < width:
        while guard.forward_pos() in object_positions:
            guard.turn_right()

        guard.move_forward()


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

def generate_movement_map(data: Data, obstacle_row: int, obstacle_col: int):
    return {
        'N': find_next_obstacle((obstacle_row + 1, obstacle_col), 'N', data),
        'E': find_next_obstacle((obstacle_row, obstacle_col - 1), 'E', data),
        'S': find_next_obstacle((obstacle_row - 1, obstacle_col), 'S', data),
        'W': find_next_obstacle((obstacle_row, obstacle_col + 1), 'W', data),
    }