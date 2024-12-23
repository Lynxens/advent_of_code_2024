from collections import defaultdict, deque
from dataclasses import dataclass
from functools import lru_cache

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    connections: dict[str, set[str]]


@advent_info(day=23)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        connections = defaultdict(set)

        for line in read_lines(file_path):
            a, b = split_once(line, '-')
            connections[a].add(b)
            connections[b].add(a)

        return Data(dict(connections))

    @expected_answers(example_answer=7, answer=1327)
    def puzzle_1(self, data: Data) -> int:
        chief_pcs = set(key for key in data.connections.keys() if key[0] == 't')

        interconnections = set()
        for chief_pc in chief_pcs:
            connecting_pcs = data.connections[chief_pc]

            for pc1 in connecting_pcs:
                pc1_connections = data.connections[pc1]
                for pc2 in connecting_pcs:
                    if pc1 == pc2:
                        continue

                    if pc2 in pc1_connections:
                        interconnections.add(tuple(sorted([chief_pc, pc1, pc2])))

        return len(interconnections)

    @expected_answers(example_answer='co,de,ka,ta', answer='df,kg,la,mp,pb,qh,sk,th,vn,ww,xp,yp,zk')
    def puzzle_2(self, data: Data) -> str:
        network = find_largest_network(data)

        @lru_cache(maxsize=None)
        def find_largest_inner_network(current: str = None, selection_str: str = '') -> str:
            connections = data.connections[current] if current else network
            selection = set(selection_str.split(',') if selection_str else [])

            inner_networks = [selection_str]
            for connected_pc in connections:
                if connected_pc in selection or not selection.issubset(data.connections[connected_pc]):
                    continue

                inner_networks.append(find_largest_inner_network(connected_pc, ','.join(sorted([*selection, connected_pc]))))

            return max(inner_networks, key=len)

        return find_largest_inner_network()

def find_largest_network(data: Data) -> set[str]:
    largest_network = set()

    visited = set()
    for pc in data.connections.keys():
        if pc in visited:
            continue

        network = set()
        queue = deque([pc])

        while queue:
            current_pc = queue.popleft()

            if current_pc in network:
                continue

            visited.add(current_pc)
            network.add(current_pc)

            for connected_pc in data.connections[current_pc]:
                if connected_pc in network:
                    continue

                queue.append(connected_pc)

        if len(network) > len(largest_network):
            largest_network = network

    return largest_network


