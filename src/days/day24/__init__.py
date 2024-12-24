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

    @expected_answers(example_answer='', answer=None)
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

            gate = data.gates[z_output]
            print(
                z_output,
                len(output_gates[z_output]),
                output_gates[z_output],
                [*map(lambda g: data.gates[g].operator, output_gates[z_output])],
                gate.operator,
                data.gates[gate.left].operator if gate.left in data.gates else gate.left,
                data.gates[gate.right].operator if gate.right in data.gates else gate.right,
            )

        for i in range(1, 45):
            node_values = dict()

            def get_node_value(node: str, swap: dict[str, str] = {}, depth: int = 0) -> bool:
                if depth > 100:
                    return False

                if node not in node_values:
                    connection = data.gates[node]
                    left_value = get_node_value(swap.get(connection.left, connection.left), swap, depth + 1)
                    right_value = get_node_value(swap.get(connection.right, connection.right), swap, depth + 1)
                    node_values[node] = OperatorHandler[connection.operator](left_value, right_value)

                return node_values[node]

            all_okay = True
            node_values = {
                k: False for k in data.inputs.keys()
            }
            node_values['x' + str(i).zfill(2)] = True
            zi = 'z' + str(i).zfill(2)
            if get_node_value(zi) != True:
                print(zi + ' 1 0 = 0')
                all_okay = False

            node_values = {
                k: False for k in data.inputs.keys()
            }
            node_values['y' + str(i).zfill(2)] = True
            if get_node_value(zi) != True:
                print(zi + ' 0 1 = 0')
                all_okay = False

            node_values = {
                k: False for k in data.inputs.keys()
            }
            node_values['x' + str(i).zfill(2)] = True
            node_values['y' + str(i).zfill(2)] = True
            if get_node_value(zi) != False:
                print(zi + ' 1 1 = 1')
                all_okay = False

            node_values = {
                k: False for k in data.inputs.keys()
            }
            node_values['x' + str(i - 1).zfill(2)] = True
            node_values['y' + str(i - 1).zfill(2)] = True
            if get_node_value(zi) != True:
                print(zi + ' --1 --1 = 0')
                all_okay = False

            if all_okay:
                continue

            potential_gates = output_gates[f'z{i:02d}'] | output_gates[f'z{(i + 1):02d}'] | {f'z{i:02d}', f'z{(i + 1):02d}'}
            for a, b in combinations(potential_gates, 2):
                swap_gates = {
                    a: b,
                    b: a,
                }

                node_values = {
                    k: False for k in data.inputs.keys()
                }
                node_values['x' + str(i).zfill(2)] = True
                if get_node_value(swap_gates.get(zi, zi), swap_gates) != True:
                    continue

                node_values = {
                    k: False for k in data.inputs.keys()
                }
                node_values['y' + str(i).zfill(2)] = True
                if get_node_value(swap_gates.get(zi, zi), swap_gates) != True:
                    continue

                node_values = {
                    k: False for k in data.inputs.keys()
                }
                node_values['x' + str(i).zfill(2)] = True
                node_values['y' + str(i).zfill(2)] = True
                if get_node_value(swap_gates.get(zi, zi), swap_gates) != False:
                    continue

                node_values = {
                    k: False for k in data.inputs.keys()
                }
                node_values['x' + str(i - 1).zfill(2)] = True
                node_values['y' + str(i - 1).zfill(2)] = True
                if get_node_value(swap_gates.get(zi, zi), swap_gates) != True:
                    continue

                print(a, b)
                # data.gates[a], data.gates[b] = data.gates[b], data.gates[a]
                # break

        return None

"""   
nbc,svm,kqk,z15,cgq,z23,z39,fnr

z05 4 {'svm', 'rgq', 'brg', 'ppw'} ['AND', 'OR', 'AND', 'AND'] XOR OR AND
z06 4 {'nbc', 'skn', 'pdf', 'wcw'} ['XOR', 'AND', 'OR', 'XOR'] XOR OR XOR
nbc svm

z15 6 {'wfh', 'pbd', 'cpv', 'wth', 'dkk', 'fwr'} ['AND', 'AND', 'OR', 'AND', 'AND', 'XOR'] OR AND AND
z16 2 {'kqk', 'rbr'} ['XOR', 'XOR'] XOR XOR XOR
kqk z15

z23 0 set() [] AND x23 y23
z24 8 {'qdg', 'jcb', 'kph', 'nkr', 'dwt', 'hpw', 'cgq', 'ngq'} ['AND', 'AND', 'OR', 'XOR', 'AND', 'XOR', 'XOR', 'OR'] XOR XOR OR
cgq z23

z39 4 {'hpf', 'bdr', 'fsp', 'phv'} ['AND', 'XOR', 'OR', 'AND'] AND OR XOR
z40 4 {'fnr', 'nqp', 'sbn', 'nrj'} ['XOR', 'XOR', 'OR', 'AND'] XOR XOR OR
z39 fnr
"""
