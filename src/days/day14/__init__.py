from dataclasses import dataclass

import numpy as np

from abstract_advent_day import *
from data_reader import *
from util import *
import re


@dataclass(slots=True)
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]


@dataclass(slots=True, frozen=True)
class Data:
    robots: list[Robot]
    width: int
    height: int


@advent_info(day=14)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        regex = re.compile(r"p=(?P<x>\d+),(?P<y>\d+) v=(?P<dx>[-\d]+),(?P<dy>[-\d]+)")

        robots = []
        for line in read_lines(file_path):
            x, y, dx, dy = regex.match(line).groups()
            robots.append(Robot(
                position=(int(y), int(x)),
                velocity=(int(dy), int(dx)),
            ))

        if "example" in file_path:
            width = 11
            height = 7
        else:
            width = 101
            height = 103

        return Data(robots, width, height)

    @expected_answers(example_answer=12, answer=230900224)
    def puzzle_1(self, data: Data) -> int:
        steps = 100
        quadrants = [0, 0, 0, 0]
        height, width = data.height, data.width

        for robot in data.robots:
            (y, x), (dy, dx) = robot.position, robot.velocity
            end_y = (y + dy * steps) % height
            end_x = (x + dx * steps) % data.width

            qh = height // 2
            qw = width // 2

            top = end_y < qh
            bottom = end_y >= height - qh
            left = end_x < qw
            right = end_x >= width - qw

            if top and left:  # Quadrant top-left
                quadrants[0] += 1
            elif top and right: # Quadrant top-right
                quadrants[1] += 1
            elif bottom and left: # Quadrant bottom-left
                quadrants[2] += 1
            elif bottom and right:  # Quadrant bottom-right
                quadrants[3] += 1

        return int(np.prod(quadrants))

    @expected_answers(example_answer=1, answer=6532)
    def puzzle_2(self, data: Data) -> int:
        steps = 0

        while len(set(robot.position for robot in data.robots)) != len(data.robots):
            for robot in data.robots:
                (y, x), (dy, dx) = robot.position, robot.velocity

                robot.position = (
                    (y + dy) % data.height,
                    (x + dx) % data.width,
                )

            steps += 1

        return steps
