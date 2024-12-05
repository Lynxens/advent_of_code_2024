from dataclasses import dataclass
from abstract_advent_day import *
from data_reader import *
from util import *
from functools import cmp_to_key


@dataclass(slots=True, frozen=True)
class Data:
    rules: list[tuple[int, int]]
    updates: list[list[int]]


@advent_info(day=5)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        rules_str, updates_str = split_once(read_full(file_path), '\n\n')

        rules = []
        for rule_str in rules_str.split('\n'):
            before, after = split_once(rule_str, '|')
            rules.append((int(before), int(after)))

        return Data(
            rules=rules,
            updates=[[*map(int, update_str.split(','))] for update_str in updates_str.split('\n')],
        )

    @expected_answers(example_answer=143, answer=4790)
    def puzzle_1(self, data: Data) -> int:
        return sum([middle(update) for update in data.updates if is_valid_update(update, data)])

    @expected_answers(example_answer=123, answer=6319)
    def puzzle_2(self, data: Data) -> int:
        cmp_pages = cmp_to_key(lambda a, b: -1 if (a, b) in data.rules else 1)
        return sum(middle(sorted(update, key=cmp_pages)) for update in data.updates if not is_valid_update(update, data))

def is_valid_update(update: list[int], data: Data) -> bool:
    for before, after in data.rules:
        try:
            index_before = update.index(before)
            index_after = update.index(after)
        except ValueError:
            continue

        if not index_before < index_after:
            return False

    return True

def middle(l: list[int]) -> int:
    return l[len(l) // 2]