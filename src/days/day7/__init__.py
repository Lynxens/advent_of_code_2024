from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    equations: list[tuple[int, list[int]]]


@advent_info(day=7)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        equations = []
        for line in read_lines(file_path):
            result, params = split_once(line, ": ")
            equations.append((int(result), [*map(int, params.split(' '))]))

        return Data(equations)

    @expected_answers(example_answer=3749, answer=465126289353)
    def puzzle_1(self, data: Data) -> int:
        return sum(
            goal
            for goal, params in data.equations
            if can_produce_valid_equation(params[0], params[1:], goal, ['*', '+'])
        )

    @expected_answers(example_answer=11387, answer=70597497486371)
    def puzzle_2(self, data: Data) -> int:
        return sum(
            goal
            for goal, params in data.equations
            if can_produce_valid_equation(params[0], params[1:], goal, ['*', '+', '||'])
        )

OPERATORS = {
    '*': lambda a, b: a * b,
    '+': lambda a, b: a + b,
    '||': lambda a, b: a * pow(10, len(str(b))) + b,
}

def can_produce_valid_equation(a: int, rest: list[int], goal: int, operators: list[str]) -> bool:
    if len(rest) == 0:
        return a == goal

    if a > goal:
        return False

    return any(
        can_produce_valid_equation(OPERATORS[operator](a, rest[0]), rest[1:], goal, operators)
        for operator in operators
    )