from dataclasses import dataclass
from enum import Enum
from typing import Callable

from abstract_advent_day import *
from data_reader import *
from util import *

Operator = Enum('AND', 'OR', 'XOR')

OperatorHandler: dict[Operator, Callable[[bool, bool], bool]] = {
    'AND': lambda left, right: left and right,
    'OR': lambda left, right: left or right,
    'XOR': lambda left, right: left ^ right,
}

@dataclass(slots=True, frozen=True)
class Gate:
    left: str
    right: str
    output: str
    operator: Operator


@dataclass(slots=True, frozen=True)
class Data:
    inputs: dict[str, bool]
    gates: dict[str, Gate]
    is_example: bool

@advent_info(day=24)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        inputs_str, gates_str = split_once(read_full(file_path), "\n\n")

        inputs = {}
        for input_str in inputs_str.splitlines():
            input_name, input_value = split_once(input_str, ': ')
            inputs[input_name] = input_value == '1'

        gates = {}
        for gate_str in gates_str.splitlines():
            logic_str, output = split_once(gate_str, ' -> ')
            left, operator, right = logic_str.split(' ')
            connection = Gate(
                left=left,
                right=right,
                output=output,
                operator=operator,
            )

            gates[output] = connection

        return Data(inputs, gates, is_example='example' in file_path)

    @expected_answers(example_answer=2024, answer=57344080719736)
    def puzzle_1(self, data: Data) -> int:
        node_values = dict(data.inputs)

        def get_node_value(node: str) -> bool:
            if node not in node_values:
                connection = data.gates[node]
                left_value = get_node_value(connection.left)
                right_value = get_node_value(connection.right)
                node_values[node] = OperatorHandler[connection.operator](left_value, right_value)

            return node_values[node]

        result = ''
        for z_output in sorted(filter(lambda k: k[0] == 'z', data.gates.keys()), reverse=True):
            result += '1' if get_node_value(z_output) else '0'

        return int(result, 2)

    @expected_answers(example_answer='', answer=None)
    def puzzle_2(self, data: Data) -> str:
        if data.is_example:
            return ''
