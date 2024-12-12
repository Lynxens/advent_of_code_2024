import operator
from collections import deque
from dataclasses import dataclass
from itertools import pairwise

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    garden: np.ndarray

type Coord = tuple[int, int]
type Edge = tuple[str, *Coord]
type Region = tuple[set[Coord], set[Edge]]

@advent_info(day=12)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data(read_str_matrix(file_path))

    @expected_answers(example_answer=1930, answer=1465968)
    def puzzle_1(self, data: Data) -> int:
        regions = cluster_regions(data.garden)
        return sum(len(coords) * len(edges) for coords, edges in regions)

    @expected_answers(example_answer=(80, 436, 236, 368, 1206), answer=897702)
    def puzzle_2(self, data: Data) -> int:
        regions = cluster_regions(data.garden)
        return sum(len(coords) * count_sides(edges) for coords, edges in regions)

def cluster_regions(garden: np.ndarray) -> list[Region]:
    regions = []

    queue = deque([(0, 0)])
    visited = set()

    # BFS per region
    while queue:
        start = queue.popleft()

        if start in visited:
            continue

        region_label = garden[start]
        region_coords = set()
        region_edges = set()
        region_queue = deque([start])

        while region_queue:
            (y, x) = region_queue.popleft()

            if (y, x) in visited:
                continue

            visited.add((y, x))
            region_coords.add((y, x))

            for direction, dy, dx in [('S', 1, 0), ('E', 0, 1), ('N', -1, 0), ('W', 0, -1)]:
                (ny, nx) = (y + dy, x + dx)

                if not in_2d_grid(garden, ny, nx):
                    region_edges.add((direction, y, x))
                    continue

                if garden[ny, nx] == region_label:
                    region_queue.append((ny, nx))
                else:
                    region_edges.add((direction, y, x))
                    queue.append((ny, nx))

        regions.append((region_coords, region_edges))

    return regions

def count_sides(edges: set[tuple[str, int, int]]) -> int:
    sides = 0

    for direction in ['N', 'E', 'S', 'W']:
        edges_in_direction = [*filter(lambda edge: edge[0] == direction, edges)]

        if len(edges_in_direction) == 0:
            continue

        if direction in ['N', 'S']:
            edges_in_direction.sort(key=operator.itemgetter(1, 2))  # Sort by row, col
            dy, dx = 0, 1  # Expected diff between edges
        else:
            edges_in_direction.sort(key=operator.itemgetter(2, 1))  # Sort by col, row
            dy, dx = 1, 0  # Expected diff between edges

        # Count non-consecutive edges in same direction
        sides += 1
        for (_, r1, c1), (_, r2, c2) in pairwise(edges_in_direction):
            if r2 - r1 != dy or c2 - c1 != dx:
                sides += 1

    return sides
