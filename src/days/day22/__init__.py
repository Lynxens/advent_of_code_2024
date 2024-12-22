from collections import defaultdict
from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    buyers: list[int]


@advent_info(day=22)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data([*map(int, read_lines(file_path))])

    @expected_answers(example_answer=37327623, answer=13429191512)
    def puzzle_1(self, data: Data) -> int:
        return sum(generate_secret_numbers(buyer)[-1] for buyer in data.buyers)

    @expected_answers(example_answer=(23,), answer=1582)
    def puzzle_2(self, data: Data) -> int:
        sequences = [generate_secret_numbers(buyer) for buyer in data.buyers]
        offers = [np.array(sequence) % 10 for sequence in sequences]
        diffs = [np.diff(offer) for offer in offers]

        window_price = defaultdict(int)
        for buyer in range(len(data.buyers)):
            diff = diffs[buyer]
            buyer_windows = set()

            for i in range(len(diff) - 3):
                window = tuple(diff[i:i + 4])

                if window in buyer_windows:
                    continue

                window_price[window] += offers[buyer][i + 4]
                buyer_windows.add(window)

        return max(window_price.values())


def generate_secret_numbers(initial: int, repeat: int = 2000) -> list[int]:
    sequence = [initial]

    for _ in range(repeat):
        n0 = sequence[-1]
        n1 = (n0 ^ (n0 * 64)) % 16777216
        n2 = (n1 ^ (n1 // 32)) % 16777216
        n3 = (n2 ^ (n2 * 2048)) % 16777216
        sequence.append(n3)

    return sequence
