from abstract_advent_day import *
from data_reader import *
from util import *


@dataclass(slots=True, frozen=True)
class Data:
    word_search: np.ndarray


@advent_info(day=4)
class AdventDay(AbstractAdventDay):
    def read(self, file_path: str) -> Data:
        lines = [list(line.rstrip()) for line in read_lines(file_path)]
        return Data(np.array(lines))

    @expected_answers(example_answer=18, answer=2468)
    def puzzle_1(self, data: Data) -> int:
        lines = implode(
            map(implode, [
                *data.word_search,  # Horizontal lines
                *data.word_search.T,  # Vertical lines
                *get_diagonal_lines(data.word_search),  # Diagonal lines
            ]),
            sep='\n',
        )

        return lines.count('XMAS') + lines.count('SAMX')

    @expected_answers(example_answer=9, answer=1864)
    def puzzle_2(self, data: Data) -> int:
        hits = 0

        for i, j in np.argwhere(data.word_search == 'A'):
            moore = moore_neighbourhood(data.word_search, i, j)

            if (
                    all(letter == 'M' or letter == 'S' for letter in [moore.NE, moore.NW, moore.SE, moore.SW])
                    and moore.NW != moore.SE
                    and moore.NE != moore.SW
            ):
                hits += 1

        return hits

def get_diagonal_lines(word_search: np.ndarray) -> list[list[str]]:
    size = word_search.shape[0]
    diagonal_lines = []

    for offset in range(size):
        # Top right triangle
        diagonal_lines.append([*word_search[(np.arange(0, size - offset), np.arange(offset, size))]])

        # Top left triangle
        diagonal_lines.append([*word_search[(np.arange(0, size - offset), np.arange(size - offset - 1, -1, -1))]])

        if offset > 0:
            # Bottom left triangle
            diagonal_lines.append([*word_search[(np.arange(offset, size), np.arange(0, size - offset))]])

            # Bottom right triangle
            diagonal_lines.append([*word_search[(np.arange(offset, size), np.arange(size - 1, offset - 1, -1))]])

    return diagonal_lines