def read_full(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()

def read_lines(file_path: str) -> list[str]:
    with open(file_path, 'r') as f:
        return f.readlines()

def split_once(s: str, sep: str) -> tuple[str, str]:
    parts = s.split(sep, 1)

    return parts[0], parts[1] if len(parts) > 1 else ''
