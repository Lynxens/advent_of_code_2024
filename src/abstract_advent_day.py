import unittest

type Answer = int | str | None

def advent_info(day: int):
    def decorator(cls: AbstractAdventDay):
        cls.day = day
        return cls

    return decorator

def expected_answers(example_answer: Answer | tuple[Answer, ...], answer: Answer | tuple[Answer, ...], disable: bool = False):
    def decorator(func: callable):
        func.example_answer = example_answer
        func.answer = answer
        func.disable = disable
        return func

    return decorator

class AbstractAdventDay(unittest.TestCase):
    __slots__ = ('day',)

    def __init__(
            self,
            method_name: str,
    ) -> None:
        super().__init__(method_name)

    def read_example(self, example_index: int|None = None) -> object:
        if example_index is None:
            return self.read(f'day{self.day}/input_example.txt')
        else:
            return self.read(f'day{self.day}/input_example_{example_index}.txt')

    def read_main(self) -> object:
        return self.read(f'day{self.day}/input.txt')

    def test_puzzle_1_example(self):
        if self.puzzle_1.disable:
            return

        if isinstance(self.puzzle_1.example_answer, tuple):
            for i, answer in enumerate(self.puzzle_1.example_answer, start=1):
                self.assertEqual(answer, self.puzzle_1(self.read_example(i)))
        else:
            self.assertEqual(self.puzzle_1.example_answer, self.puzzle_1(self.read_example()))

    def test_puzzle_1_real(self):
        if self.puzzle_1.disable:
            return

        self.assertEqual(self.puzzle_1.answer, self.puzzle_1(self.read_main()))

    def test_puzzle_2_example(self):
        if self.puzzle_2.disable:
            return

        if isinstance(self.puzzle_2.example_answer, tuple):
            for i, answer in enumerate(self.puzzle_2.example_answer, start=1):
                self.assertEqual(answer, self.puzzle_2(self.read_example(i)))
        else:
            self.assertEqual(self.puzzle_2.example_answer, self.puzzle_2(self.read_example()))

    def test_puzzle_2_real(self):
        if self.puzzle_2.disable:
            return

        self.assertEqual(self.puzzle_2.answer, self.puzzle_2(self.read_main()))

    def solve_puzzles(self):
        print(f"Puzzle 1: {self.puzzle_1(self.read_main())}")
        print(f"Puzzle 2: {self.puzzle_2(self.read_main())}")

    def read(self, file_path: str) -> object:
        raise NotImplementedError

    @expected_answers(example_answer=None, answer=None)
    def puzzle_1(self, *args):
        raise NotImplementedError

    @expected_answers(example_answer=None, answer=None)
    def puzzle_2(self, *args):
        raise NotImplementedError