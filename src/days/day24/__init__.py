from dataclasses import dataclass
from enum import Enum
from itertools import combinations
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

    @expected_answers(example_answer='', answer='cgq,fnr,kqk,nbc,svm,z15,z23,z39')
    def puzzle_2(self, data: Data) -> str:
        if data.is_example:
            return ''

        output_gates = {}
        def find_output_gates(node: str, ignore: set[str]) -> set[str]:
            if node in data.inputs or node in ignore:
                return set()

            if node not in output_gates:
                gate = data.gates[node]
                left_gates = find_output_gates(gate.left, ignore)
                right_gates = find_output_gates(gate.right, ignore)
                output_gates[node] = left_gates | right_gates

            return output_gates[node] | {node}

        visited = set()
        for z_output in sorted(filter(lambda k: k[0] == 'z', data.gates.keys())):
            visited |= find_output_gates(z_output, visited)

        swapped_gates = {}
        for i in range(1, 45):
            if output_works_as_expected(data, i, swapped_gates):
                continue

            zi = f'z{i:02d}'
            zi_plus = f'z{(i + 1):02d}'
            potential_gates = {zi} | output_gates[zi] | output_gates[zi_plus]
            for a, b in combinations(potential_gates, 2):
                test_swap = swapped_gates | {
                    a: b,
                    b: a,
                }

                if output_works_as_expected(data, i, test_swap) and output_works_as_expected(data, i + 1, test_swap):
                    swapped_gates = test_swap
                    break

        return ','.join(sorted(swapped_gates.keys()))


def output_works_as_expected(data: Data, i: int, swap: dict[str, str]) -> bool:
    xi = f'x{i:02d}'
    yi = f'y{i:02d}'
    zi = f'z{i:02d}'
    xi_min = f'x{(i - 1):02d}'
    yi_min = f'y{(i - 1):02d}'
    zi_plus = f'z{(i + 1):02d}'

    return (
        get_output_value(data, swap, zi, [xi]) == True
        and get_output_value(data, swap, zi, [yi]) == True
        and get_output_value(data, swap, zi, [xi, yi]) == False
        and get_output_value(data, swap, zi_plus, [xi, yi]) == True
        and get_output_value(data, swap, zi_plus, [xi]) == False
        and get_output_value(data, swap, zi_plus, [yi]) == False
        and get_output_value(data, swap, zi, [xi_min, yi_min]) == True
        and get_output_value(data, swap, zi, [xi_min]) == False
        and get_output_value(data, swap, zi, [yi_min]) == False
    )

def get_output_value(data: Data, swap: dict[str, str], output: str, true_inputs: list[str]) -> bool:
    node_values = {
        k: k in true_inputs for k in data.inputs.keys()
    }

    def get_node_value(node: str, depth: int = 0) -> bool:
        if depth > 100:
            return False

        if node not in node_values:
            connection = data.gates[node]
            left_value = get_node_value(swap.get(connection.left, connection.left), depth + 1)
            right_value = get_node_value(swap.get(connection.right, connection.right), depth + 1)
            node_values[node] = OperatorHandler[connection.operator](left_value, right_value)

        return node_values[node]

    return get_node_value(swap.get(output, output))
