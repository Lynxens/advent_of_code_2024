import numpy as np


def read_full(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()


def read_lines(file_path: str) -> list[str]:
    with open(file_path, 'r') as f:
        return [line.rstrip() for line in f.readlines()]


def read_int_matrix(file_path: str, sep: str = ' ') -> np.ndarray:
    return np.array([*map(
        lambda line: [*map(int, line.split(sep) if sep else list(line))],
        read_lines(file_path),
    )])


def read_str_matrix(file_path: str) -> np.ndarray:
    return np.array([*map(
        lambda line: [*line],
        read_lines(file_path),
    )])

def str_to_str_matrix(s: str) -> np.ndarray:
    return np.array([*map(
        lambda line: [*line],
        s.split('\n'),
    )])

def int_array(s: str) -> np.ndarray:
    return np.array(
        [*map(int, s.split(' '))],
        dtype=np.int64,
    )


def split_once(s: str, sep: str) -> tuple[str, str]:
    parts = s.split(sep, 1)

    return parts[0], parts[1] if len(parts) > 1 else ''
