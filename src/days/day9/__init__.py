from dataclasses import dataclass

import numpy as np

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    disk_map: list[int]

@dataclass(slots=True)
class Entry:
    size: int
    is_space: bool = False

class Space(Entry):
    def __init__(self, size: int):
        super().__init__(id=None, size=size, is_space=True)

class File(Entry):
    def __init__(self, file_id: int, size: int):
        super().__init__(id=file_id, size=size, is_space=False)

@dataclass(slots=True)
class Disk:
    memory: list[Entry]

    def __init__(self, disk_map: list[int]):
        self.memory = []

        file_id = 0
        for i in range(len(disk_map)):
            if i % 2 == 0:
                self.memory.append(File(file_id=file_id, size=disk_map[i]))
                file_id += 1
            else:
                self.memory.append(Space(size=disk_map[i]))

    def files(self):
        return [*filter(lambda entry: not entry.is_space, reversed(self.memory))]

    def find_space(self, size: int) -> int | None:
        for i in range(len(self.memory)):
            if self.memory[i].is_space and self.memory[i].size >= size:
                return i

    def find_file_index(self, file_id: int, start_index: int) -> int:
        for i in range(start_index, -1, -1):
            if self.memory[i].id == file_id:
                return i

    def move_file(self, from_index: int, to_index: int):
        file = self.memory[from_index]

        if 0 < from_index < len(self.memory) - 1 and self.memory[from_index - 1].is_space and self.memory[from_index + 1].is_space:
            self.memory[from_index - 1].size += self.memory[from_index + 1].size + file.size
            del self.memory[from_index + 1]
            del self.memory[from_index]
        elif self.memory[from_index - 1].is_space:
            self.memory[from_index - 1].size += file.size
            del self.memory[from_index]
        elif self.memory[from_index + 1].is_space:
            self.memory[from_index + 1].size += file.size
            del self.memory[from_index]
        else:
            self.memory[from_index] = Space(size=file.size)

        self.memory[to_index].size -= file.size

        self.memory.insert(to_index, file)

    def calculate_checksum(self) -> int:
        checksum = 0
        position = 0

        for entry in self.memory:
            if entry.is_space:
                position += entry.size
            else:
                for _ in range(entry.size):
                    checksum += entry.id * position
                    position += 1

        return checksum


@advent_info(day=9)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        return Data([*map(int, read_full(file_path))])

    @expected_answers(example_answer=1928, answer=6331212425418)
    def puzzle_1(self, data: Data) -> int:
        file_sizes = np.array(data.disk_map)[::2]
        free_spaces = np.array(data.disk_map)[1::2]
        files = [*zip(np.arange(len(file_sizes)), file_sizes)]

        checksum = 0
        position = 0

        for i, free_space in enumerate(free_spaces):
            next_file_id, next_file_size = files[0]

            for _ in range(next_file_size):
                checksum += next_file_id * position
                position += 1

            del files[0]

            for _ in range(free_space):
                if len(files) == 0:
                    return int(checksum)

                last_file_id, last_file_size = files[-1]

                checksum += last_file_id * position
                position += 1

                if last_file_size == 1:
                    del files[-1]
                else:
                    files[-1] = (last_file_id, last_file_size - 1)

        return int(checksum)

    @expected_answers(example_answer=2858, answer=6363268339304)
    def puzzle_2(self, data: Data) -> int:
        disk = Disk(data.disk_map)

        last_index = len(disk.memory) - 1
        for file in disk.files():
            to_index = disk.find_space(file.size)

            if to_index is None:
                continue

            from_index = disk.find_file_index(file.id, last_index)

            if from_index <= to_index:
                continue

            disk.move_file(from_index, to_index)
            last_index = from_index

        return disk.calculate_checksum()
