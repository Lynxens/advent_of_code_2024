from dataclasses import dataclass

import numpy as np

from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    disk_map: list[int]


@dataclass(slots=True)
class File:
    id: int
    size: int


@dataclass(slots=True)
class Space:
    size: int


@dataclass(slots=True)
class Disk:
    memory: list[File | Space]

    def files(self):
        return [*filter(lambda entry: isinstance(entry, File), reversed(self.memory))]

    def find_space(self, size: int) -> int | None:
        for i, entry in enumerate(self.memory):
            if isinstance(entry, Space) and entry.size >= size:
                return i

    def move_file(self, from_index: int, to_index: int):
        file = self.memory[from_index]

        if 0 < from_index < len(self.memory) - 1 and isinstance(self.memory[from_index - 1], Space) and isinstance(
                self.memory[from_index + 1], Space):
            self.memory[from_index - 1].size += self.memory[from_index + 1].size + file.size
            del self.memory[from_index + 1]
            del self.memory[from_index]
        elif isinstance(self.memory[from_index - 1], Space):
            self.memory[from_index - 1].size += file.size
            del self.memory[from_index]
        elif isinstance(self.memory[from_index + 1], Space):
            self.memory[from_index + 1].size += file.size
            del self.memory[from_index]
        else:
            self.memory[from_index] = Space(file.size)

        self.memory[to_index].size -= file.size

        self.memory.insert(to_index, file)

    def calculate_checksum(self) -> int:
        checksum = 0
        position = 0

        for entry in self.memory:
            if isinstance(entry, File):
                for _ in range(entry.size):
                    checksum += entry.id * position
                    position += 1
            else:
                for _ in range(entry.size):
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
        memory = []

        file_id = 0
        for i in range(len(data.disk_map)):
            if i % 2 == 0:
                memory.append(File(id=file_id, size=data.disk_map[i]))
                file_id += 1
            else:
                memory.append(Space(size=data.disk_map[i]))

        disk = Disk(memory)

        for file in disk.files():
            to_index = disk.find_space(file.size)

            if to_index is None:
                continue

            from_index = disk.memory.index(file)

            if from_index <= to_index:
                continue

            disk.move_file(from_index, to_index)

        return disk.calculate_checksum()
