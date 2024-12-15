from collections import deque
from dataclasses import dataclass

import numpy as np

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    grid: np.ndarray
    moves: list[np.ndarray]

Moves = {
    '^': np.array([-1, 0]),
    'v': np.array([1, 0]),
    '<': np.array([0, -1]),
    '>': np.array([0, 1]),
}

@advent_info(day=15)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        grid_s, moves_s = split_once(read_full(file_path), '\n\n')
        moves = [Moves[move] for move in moves_s if move != "\n"]

        return Data(
            grid=str_to_str_matrix(grid_s),
            moves=moves,
        )

    @expected_answers(example_answer=(2028, 10092), answer=1413675)
    def puzzle_1(self, data: Data) -> int:
        robot_pos = np.argwhere(data.grid == '@')[0]
        boxes = [*map(tuple, np.argwhere(data.grid == 'O'))]

        for dydx in data.moves:
            lookahead = robot_pos + dydx

            boxes_to_move = set()
            while True:
                try:
                    box_index = boxes.index(tuple(lookahead))
                    boxes_to_move.add(box_index)
                    lookahead += dydx
                except ValueError:
                    break

            if not in_2d_grid(data.grid, *lookahead) or data.grid[*lookahead] == '#':
                continue

            for box_index in boxes_to_move:
                (y, x) = boxes[box_index]
                boxes[box_index] = (y + dydx[0], x + dydx[1])

            robot_pos += dydx

        return sum(y * 100 + x for y, x in boxes)


    @expected_answers(example_answer=9021, answer=1399772)
    def puzzle_2(self, data: Data) -> int:
        grid = np.zeros((data.grid.shape[0], data.grid.shape[1] * 2), dtype=str)
        grid.fill('.')

        for r in range(data.grid.shape[0]):
            for c in range(data.grid.shape[1]):
                v = data.grid[r, c]

                if v == '#':
                    grid[r, c * 2] = '#'
                    grid[r, c * 2 + 1] = '#'
                elif v == 'O':
                    grid[r, c * 2] = '['
                    grid[r, c * 2 + 1] = ']'
                elif v == '@':
                    grid[r, c * 2] = '@'

        robot_pos = np.argwhere(grid == '@')[0]
        boxes_l = [*map(tuple, np.argwhere(grid == '['))]
        boxes_r = [*map(tuple, np.argwhere(grid == ']'))]

        for dydx in data.moves:
            boxes_to_move, has_obstruction = find_boxes_to_move(robot_pos, dydx, grid, boxes_l, boxes_r)

            if has_obstruction:
                continue

            for box_index in boxes_to_move:
                (ly, lx) = boxes_l[box_index]
                (ry, rx) = boxes_r[box_index]
                boxes_l[box_index] = (ly + dydx[0], lx + dydx[1])
                boxes_r[box_index] = (ry + dydx[0], rx + dydx[1])

            robot_pos += dydx

        return sum(y * 100 + x for y, x in boxes_l)

def find_boxes_to_move(
        robot_pos: np.ndarray,
        dydx: np.ndarray,
        grid: np.ndarray,
        boxes_l: list[tuple[int, int]],
        boxes_r: list[tuple[int, int]],
) -> tuple[set[int], bool]:
    queue = deque([robot_pos + dydx])
    boxes_to_move = set()

    while queue:
        pos = queue.popleft()

        if not in_2d_grid(grid, *pos) or grid[*pos] == '#':
            return set(), True

        pos_t = tuple(pos)
        if pos_t in boxes_l or pos_t in boxes_r:
            try:
                index = boxes_l.index(pos_t)
            except ValueError:
                index = boxes_r.index(pos_t)

            if index in boxes_to_move:
                continue

            boxes_to_move.add(index)
            queue.append(np.array([*boxes_l[index]]) + dydx)
            queue.append(np.array([*boxes_r[index]]) + dydx)

    return boxes_to_move, False