def read_file(file_path: str, mode: str = "r") -> str:
    with open(file_path, mode, encoding="utf-8") as f:
        return f.read()


def save_to_file(text: str, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
