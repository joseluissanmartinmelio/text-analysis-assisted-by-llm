import os
import time
import textwrap
from pathlib import Path
import pypandoc
from src.pdf_reader import extract_text_without_footer_header as extract_text_pdf
from src.docx_reader import extract_text_without_footer_header as extract_text_docx
from src.txt_reader import extract_text_without_footer_header as extract_text_txt
from src.word_stats import count_words
from src.ai_claude_4 import ai_assistant as ai_assistant_claude
from src.ai_deepseek_r1 import ai_assistant as ai_assistant_deepseek
from src.ai_openai_o3 import ai_assistant as ai_assistant_openai_o3
from src.ai_openai_o4_mini import ai_assistant as ai_assistant_openai_o4_mini

AI_MODELS = {
    "claude": ai_assistant_claude,
    "deepseek": ai_assistant_deepseek,
    "openai_o3": ai_assistant_openai_o3,
    "openai_o4_mini": ai_assistant_openai_o4_mini,
}


def get_ai_assistant(model_name):
    if model_name not in AI_MODELS:
        raise ValueError(
            f"Model {model_name} not supported. Available models: {list(AI_MODELS.keys())}"
        )
    return AI_MODELS[model_name]


def run_analysis(uploaded_file, prompt_template_text, selected_model, question="", theme="", keyword=""):
    results = {}
    temp_filename = uploaded_file.filename
    uploaded_file.save(temp_filename)
    text = ""

    try:
        if temp_filename.endswith(".pdf"):
            text = extract_text_pdf(temp_filename)
        elif temp_filename.endswith(".docx"):
            text = extract_text_docx(temp_filename)
        elif temp_filename.endswith(".txt"):
            text = extract_text_txt(temp_filename)
        else:
            raise ValueError("Unsupported file format. Use .pdf, .docx, or .txt")

        results["extracted_text"] = text
        results["text_stats"] = count_words(text)

        prompt_template = textwrap.dedent(prompt_template_text)
        
        format_dict = {
            'context': text,
            'question': question,
            'theme': theme,
            'keyword': keyword
        }
        
        import re
        variables_in_template = re.findall(r'\{(\w+)\}', prompt_template)
        
        filtered_dict = {}
        for var in variables_in_template:
            if var in format_dict:
                filtered_dict[var] = format_dict[var]
        
        final_prompt = prompt_template.format(**filtered_dict)

        ai_assistant = get_ai_assistant(selected_model)
        response = ai_assistant(final_prompt)

        results["ai_response"] = response
        results["response_stats"] = count_words(response)

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
    return output_dir / f"{input_file.stem}.md"


def process_single_file_batch(
    file_path: Path, extractor, prompt_template: str, output_dir: Path, ai_assistant, question="", theme="", keyword=""
):
    print(f"Procesando: {file_path.name}...")
    try:
        text = extractor(str(file_path))

        format_dict = {
            'context': text,
            'question': question,
            'theme': theme,
            'keyword': keyword
        }
        
        import re
        variables_in_template = re.findall(r'\{(\w+)\}', prompt_template)
        
        filtered_dict = {}
        for var in variables_in_template:
            if var in format_dict:
                filtered_dict[var] = format_dict[var]
        
        final_prompt = textwrap.dedent(prompt_template).format(**filtered_dict)
        response = ai_assistant(final_prompt)

        output_path = build_output_path(file_path, output_dir)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response)

        print(f"Guardado en: {output_path.name}")
    except Exception as e:
        print(f"Error procesando {file_path.name}: {e}")


def process_folder_batch(
    folder_path: str,
    output_dir: str,
    file_extension: str,
    prompt_template: str,
    selected_model: str,
    question: str = "",
    theme: str = "",
    keyword: str = "",
):
    folder = Path(folder_path).expanduser()
    output_path = Path(output_dir).expanduser()
    ext = file_extension.lower()

    if not folder.is_dir():
        raise FileNotFoundError(f"The input folder does not exist: {folder}")

    output_path.mkdir(parents=True, exist_ok=True)

    extractor = select_extractor(ext)

    ai_assistant = get_ai_assistant(selected_model)

    files_to_process = sorted([p for p in folder.iterdir() if p.suffix.lower() == ext])

    if not files_to_process:
        return "No files with the specified extension were found in the folder."

    start_time = time.time()
    files_processed_count = 0

    for file_path in files_to_process:
        process_single_file_batch(
            file_path, extractor, prompt_template, output_path, ai_assistant, question, theme, keyword
        )
        files_processed_count += 1

    total_time = (time.time() - start_time) / 60

    summary = (
        f"Process completed in {total_time:.2f} minutes.\n"
        f"{files_processed_count} files were processed.\n"
        f"The results were saved in: {output_path}"
    )

    print(summary)
    return summary


def create_consolidated_markdown(source_path, output_file):
    """
    Consolida todos los archivos .md de un directorio en un solo archivo markdown
    """
    source_dir = Path(source_path)
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Error: The directory '{source_path}' does not exist.")

    markdown_files = sorted(
        [f for f in source_dir.glob("*.md") if f.name != Path(output_file).name]
    )

    if not markdown_files:
        raise FileNotFoundError(f"No .md files found in '{source_path}'.")

    print(f".md files found: {[f.name for f in markdown_files]}")

    with open(output_file, "w", encoding="utf-8") as outfile:
        for md_file in markdown_files:
            print(f"Processing: {md_file.name}")
            
            title = md_file.stem
            
            outfile.write(f"# {title}\n\n")
            outfile.write(md_file.read_text(encoding="utf-8"))
            outfile.write("\n\n---\n\n")

    print(f"\nConsolidated file '{output_file}' created successfully.")
    return True


def convert_markdown_to_pdf(md_file, pdf_file):
    """
    Convierte un archivo markdown a PDF usando pypandoc
    """
    print(f"Starting conversion from '{md_file}' to '{pdf_file}'...")
    try:
        pypandoc.convert_file(
            md_file,
            "pdf",
            outputfile=pdf_file,
            extra_args=["--pdf-engine=xelatex", "-V", "geometry:margin=1in"],
        )
        print(f"PDF file '{pdf_file}' created successfully.")
        return True
    except OSError:
        raise OSError(
            "Could not find 'pandoc'. Please install pandoc on your system to generate the PDF. "
            "On Windows, download from https://pandoc.org/installing.html"
        )
    except Exception as e:
        raise Exception(f"An error occurred during PDF conversion: {e}")


def unify_markdowns_and_create_pdf(output_dir):
    """
    Función principal que unifica todos los markdowns de un directorio y genera un PDF
    """
    output_path = Path(output_dir)
    if not output_path.is_dir():
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")
    
    consolidated_md_file = output_path / "consolidated_analysis.md"
    consolidated_pdf_file = output_path / "consolidated_analysis.pdf"
    
    # Crear el markdown consolidado
    create_consolidated_markdown(str(output_path), str(consolidated_md_file))
    
    # Intentar crear el PDF
    try:
        convert_markdown_to_pdf(str(consolidated_md_file), str(consolidated_pdf_file))
        return {
            "success": True,
            "markdown_file": str(consolidated_md_file),
            "pdf_file": str(consolidated_pdf_file),
            "message": "Consolidated markdown and PDF created successfully"
        }
    except OSError as e:
        # Si falla el PDF por falta de pandoc, al menos devolvemos el markdown
        return {
            "success": True,
            "markdown_file": str(consolidated_md_file),
            "pdf_file": None,
            "message": f"Consolidated markdown created successfully. PDF generation failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": True,
            "markdown_file": str(consolidated_md_file),
            "pdf_file": None,
            "message": f"Consolidated markdown created successfully. PDF generation failed: {str(e)}"
        }
