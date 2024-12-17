import sys
from dataclasses import dataclass
from itertools import batched
from typing import Callable, Generator

from abstract_advent_day import *
from data_reader import *
from util import *

@dataclass(slots=True, frozen=True)
class Data:
    init_a: int
    program: list[int]


@advent_info(day=17)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        register_lines, program_line = split_once(read_full(file_path), '\n\n')

        return Data(
            init_a=int(split_once(register_lines.split('\n')[0], ': ')[1]),
            program=[*map(int, split_once(program_line, ': ')[1].split(','))],
        )

    @expected_answers(example_answer='4,6,3,5,6,3,5,2,1,0', answer='2,1,4,7,6,0,3,1,4')
    def puzzle_1(self, data: Data) -> str:
        return ','.join(map(str,run_program(data.init_a, data.program)))

    @expected_answers(example_answer=(117440,), answer=266932601404433)
    def puzzle_2(self, data: Data) -> int:
        def find_duplicating_program(
                index: int = len(data.program) - 1,
                base: int = 0,
        ) -> int|None:
            if index == -1:
                return base

            target = data.program[index]

            for A in range(base * 8, (base + 1) * 8):
                if next(run_program(A, data.program)) == target:
                    result = find_duplicating_program(index - 1, A)
                    if result is not None:
                        return result

            return None

        return find_duplicating_program()

def run_program(init_a: int, program: list[int]) -> Generator[int]:
    registers = {
        'A': init_a,
        'B': 0,
        'C': 0,
    }

    combo: dict[int, Callable[[], int]] = {
        0: lambda: 0,
        1: lambda: 1,
        2: lambda: 2,
        3: lambda: 3,
        4: lambda: registers['A'],
        5: lambda: registers['B'],
        6: lambda: registers['C'],
    }

    instruction: dict[int, Callable[[int, int], tuple[str, int, int]]] = {
        0: lambda o, p: ('A', registers['A'] // pow(2, combo[o]()), p + 2),  # adv
        1: lambda o, p: ('B', registers['B'] ^ o, p + 2),  # bxl
        2: lambda o, p: ('B', combo[o]() % 8, p + 2),  # bst
        3: lambda o, p: ('A', registers['A'], (p + 2) if registers['A'] == 0 else o),  # jnz
        4: lambda o, p: ('B', registers['B'] ^ registers['C'], p + 2),  # bxc
        5: lambda o, p: ('OUT', combo[o]() % 8, p + 2),  # out
        6: lambda o, p: ('B', registers['A'] // pow(2, combo[o]()), p + 2),  # bdv
        7: lambda o, p: ('C', registers['A'] // pow(2, combo[o]()), p + 2),  # cdv
    }

    pointer = 0
    while pointer < len(program):
        opcode, operand = program[pointer], program[pointer + 1]

        location, value, pointer = instruction[opcode](operand, pointer)

        if location == 'OUT':
            yield value
        else:
            registers[location] = value