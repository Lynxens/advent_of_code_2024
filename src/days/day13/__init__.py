from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *
import re
from numpy.linalg import det

@dataclass(slots=True, frozen=True)
class Machine:
    ax: int
    ay: int
    bx: int
    by: int
    x: int
    y: int

@dataclass(slots=True, frozen=True)
class Data:
    machines: list[Machine]

@advent_info(day=13)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        regex = re.compile(r"Button A: X\+(?P<ax>\d+), Y\+(?P<ay>\d+)\nButton B: X\+(?P<bx>\d+), Y\+(?P<by>\d+)\nPrize: X=(?P<x>\d+), Y=(?P<y>\d+)", re.MULTILINE)

        machines = []
        for section in read_full(file_path).split('\n\n'):
            ax, ay, bx, by, x, y = regex.search(section).groups()
            machines.append(Machine(int(ax), int(ay), int(bx), int(by), int(x), int(y)))

        return Data(machines)

    @expected_answers(example_answer=480, answer=36870)
    def puzzle_1(self, data: Data) -> int:
        return sum(
            count_tokens(*find_intersection(m.ax, m.ay, m.bx, m.by, m.x, m.y))
            for m in data.machines
        )

    @expected_answers(example_answer=875318608908, answer=78101482023732)
    def puzzle_2(self, data: Data) -> int:
        return sum(
            count_tokens(*find_intersection(m.ax, m.ay, m.bx, m.by, m.x + 10000000000000, m.y + 10000000000000))
            for m in data.machines
        )

def find_intersection(ax: int, ay: int, bx: int, by: int, x: int, y: int) -> tuple[int, int]:
    # Cramer's rule
    divisor = det(np.array([
        [ax, bx],
        [ay, by],
    ]))

    a = round(det(np.array([
        [x, bx],
        [y, by],
    ])) / divisor)

    b = round(det(np.array([
        [ax, x],
        [ay, y],
    ])) / divisor)

    if a * ax + b * bx == x and a * ay + b * by == y:
        return a, b
    else:
        return 0, 0

count_tokens = lambda a, b: a * 3 + b