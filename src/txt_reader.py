from pathlib import Path


def extract_text_without_footer_header(txt_path: str) -> str:

    txt_file = Path(txt_path)

    if not txt_file.is_file():
        raise FileNotFoundError(f"File not found: {txt_path}")

    with txt_file.open(encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_text = "".join(line.rstrip("\n") + "\n" for line in lines)

    return cleaned_text
