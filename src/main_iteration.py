import time
from pathlib import Path

from pdf_reader import extract_text_without_footer_header as extract_text_pdf
from docx_reader import extract_text_without_footer_header as extract_text_docx
from txt_reader import extract_text_without_footer_header as extract_text_txt

from ai_claude_4 import ai_assistant as ai_assistant_claude
from ai_deepseek_r1 import ai_assistant as ai_assistant_deepseek
from ai_openai_o3 import ai_assistant as ai_assistant_openai_o3
from ai_openai_o4_mini import ai_assistant as ai_assistant_openai_o4_mini

from utils import save_to_file
from prompt_loader import load_prompt

CONFIG = {
    "FOLDER_PATH": "",
    "FILE_EXTENSION": ".pdf",
    "PROMPT_PATH": "",
    "OUTPUT_DIR": "",
}


def select_extractor(extension: str):

    if extension == ".pdf":
        return extract_text_pdf
    if extension == ".txt":
        return extract_text_txt
    if extension == ".docx":
        return extract_text_docx
    raise ValueError(f"Unsupported extension: {extension}")


def build_output_path(input_file: Path, output_dir: Path) -> Path:

    return output_dir / f"{input_file.stem}_extraction.md"


def process_file(file_path: Path, extractor, prompt_path: Path, output_dir: Path):

    text = extractor(str(file_path))

    prompt = load_prompt(str(prompt_path), text)

    response = ai_assistant_deepseek(prompt)

    output_path = build_output_path(file_path, output_dir)

    save_to_file(response, str(output_path))


def main():
    cfg = CONFIG
    folder = Path(cfg["FOLDER_PATH"]).expanduser()
    output_dir = Path(cfg["OUTPUT_DIR"]).expanduser()
    ext = cfg["FILE_EXTENSION"].lower()

    if not folder.is_dir():
        raise FileNotFoundError(f"The folder {folder} does not exist.")
    if ext not in {".pdf", ".txt", ".docx"}:
        raise ValueError("FILE_EXTENSION must be .pdf, .txt, or .docx")

    output_dir.mkdir(parents=True, exist_ok=True)

    extractor = select_extractor(ext)
    files = sorted(p for p in folder.iterdir() if p.suffix.lower() == ext)

    if not files:
        print(f"No {ext} files found in {folder}")
        return

    start = time.time()

    for file_path in files:
        process_file(file_path, extractor, Path(cfg["PROMPT_PATH"]), output_dir)

    total_minutes = (time.time() - start) / 60
    print(f"{total_minutes:.2f}")


if __name__ == "__main__":
    main()
