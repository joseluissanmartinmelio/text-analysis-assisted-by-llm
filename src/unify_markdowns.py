import os
from pathlib import Path
import pypandoc
import sys

path = ""

SOURCE_FOLDER_PATH = f"{path}"

CONSOLIDATED_MD_FILE = f"{path}/consolidado.md"
CONSOLIDATED_PDF_FILE = f"{path}/consolidado.pdf"


def create_consolidated_markdown(source_path, output_file):
    source_dir = Path(source_path)
    if not source_dir.is_dir():
        print(f"Error: The directory '{source_path}' does not exist.")
        sys.exit(1)

    markdown_files = sorted(
        [f for f in source_dir.glob("*.md") if f.name != Path(output_file).name]
    )

    if not markdown_files:
        print(f"No .md files found in '{source_path}'.")
        return False

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
    print(f"Starting conversion from '{md_file}' to '{pdf_file}'...")
    try:
        pypandoc.convert_file(
            md_file,
            "pdf",
            outputfile=pdf_file,
            extra_args=["--pdf-engine=xelatex", "-V", "geometry:margin=1in"],
        )
        print(f"PDF file '{pdf_file}' created successfully.")
    except OSError:
        print("\nError: Could not find 'pandoc'.")
        print("Please install pandoc on your system to generate the PDF.")
        print("On Ubuntu/Debian, you can use: sudo apt-get install pandoc")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during PDF conversion: {e}")
        sys.exit(1)


def main():
    # sudo apt-get update for ubuntu
    # sudo apt-get install pandoc for ubuntu
    # sudo apt-get install texlive-xetex texlive-fonts-recommended for ubuntu

    if create_consolidated_markdown(SOURCE_FOLDER_PATH, CONSOLIDATED_MD_FILE):
        convert_markdown_to_pdf(CONSOLIDATED_MD_FILE, CONSOLIDATED_PDF_FILE)


if __name__ == "__main__":
    main()
