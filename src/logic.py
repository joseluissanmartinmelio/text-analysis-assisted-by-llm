import os
import time
import textwrap
from pathlib import Path

from src.pdf_reader import extract_text_without_footer_header as extract_text_pdf
from src.docx_reader import extract_text_without_footer_header as extract_text_docx
from src.txt_reader import extract_text_without_footer_header as extract_text_txt
from src.word_stats import count_words
from src.ai_module import ai_assistant

def run_analysis(uploaded_file, prompt_template_text):
    results = {}
    temp_filename = uploaded_file.filename
    uploaded_file.save(temp_filename)

    text = ""
    try:
        if temp_filename.endswith('.pdf'):
            text = extract_text_pdf(temp_filename)
        elif temp_filename.endswith('.docx'):
            text = extract_text_docx(temp_filename)
        elif temp_filename.endswith('.txt'):
            text = extract_text_txt(temp_filename)
        else:
            raise ValueError("Unsupported file format. Use .pdf, .docx, or .txt")

        results['extracted_text'] = text
        results['text_stats'] = count_words(text)

        prompt_template = textwrap.dedent(prompt_template_text)
        final_prompt = prompt_template.format(context=text)
        
        response = ai_assistant(final_prompt)
        results['ai_response'] = response
        results['response_stats'] = count_words(response)
    
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    return results

def select_extractor(extension: str):
    if extension == ".pdf":
        return extract_text_pdf
    if extension == ".txt":
        return extract_text_txt
    if extension == ".docx":
        return extract_text_docx
    raise ValueError(f"Unsupported extension: {extension}")

def build_output_path(input_file: Path, output_dir: Path) -> Path:
    return output_dir / f"{input_file.stem}_ia_response.md"

def process_single_file_batch(file_path: Path, extractor, prompt_template: str, output_dir: Path):
    print(f"Procesando: {file_path.name}...")
    try:
        text = extractor(str(file_path))
        final_prompt = textwrap.dedent(prompt_template).format(context=text)
        response = ai_assistant(final_prompt)
        output_path = build_output_path(file_path, output_dir)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response)
        print(f"Guardado en: {output_path.name}")
    except Exception as e:
        print(f"Error procesando {file_path.name}: {e}")

def process_folder_batch(folder_path: str, output_dir: str, file_extension: str, prompt_template: str):
    folder = Path(folder_path).expanduser()
    output_path = Path(output_dir).expanduser()
    ext = file_extension.lower()

    if not folder.is_dir():
        raise FileNotFoundError(f"The input folder does not exist: {folder}")

    output_path.mkdir(parents=True, exist_ok=True)

    extractor = select_extractor(ext)
    files_to_process = sorted([p for p in folder.iterdir() if p.suffix.lower() == ext])

    if not files_to_process:
        return "No files with the specified extension were found in the folder."

    start_time = time.time()
    files_processed_count = 0
    for file_path in files_to_process:
        process_single_file_batch(file_path, extractor, prompt_template, output_path)
        files_processed_count += 1
    
    total_time = (time.time() - start_time) / 60
    
    summary = (
        f"Process completed in {total_time:.2f} minutes.\n"
        f"{files_processed_count} files were processed.\n"
        f"The results were saved in: {output_path}"
    )
    print(summary)
    return summary