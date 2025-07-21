from pdf_reader import extract_text_without_footer_header as extract_text_pdf
from docx_reader import extract_text_without_footer_header as extract_text_docx
from txt_reader import extract_text_without_footer_header as extract_text_txt
from word_stats import count_words
from ai_module import ai_assistant
from utils import save_to_file
from prompt_loader import load_prompt
import os
import time

start = time.time()
if __name__ == "__main__":
    author_year = ""
    pdf_path = f"{author_year}.pdf"
    # txt_path = f"{author_year}.txt" # to read txt files
    # docx_path = f"{author_year}.docx" # to read docx files
    output_path = f""
    prompt_path = f"{author_year}_ia_response.md"

    # text = extract_text_txt(txt_path) # to read txt files
    text = extract_text_pdf(pdf_path) # to read pdf files
    # text = extract_text_docx(docx_path) # to read docx files
    print("\nExtracted Text\n")
    print(text)

    # join the text

    stats = count_words(text)
    print("\nText Statistics")
    print(f"Total words: {stats['total']}")
    print(f"Unique words: {stats['unique']}")
    print("Most common words:")
    for word, count in stats['most_common']:
        print(f"  {word}: {count}")

    prompt = load_prompt(prompt_path, text)

    response = ai_assistant(prompt)
    print("\nAI Response\n")
    print(response)

    stats_response = count_words(response)
    print("\nResponse Statistics")
    print(f"Total words: {stats_response['total']}")
    print(f"Unique words: {stats_response['unique']}")
    print("Most common words:")
    for word, count in stats_response['most_common']:
        print(f"  {word}: {count}")

    save_to_file(response, output_path)

end = time.time()
minutes = (end - start) / 60
print(f"\nExecution time: {minutes:.2f} minutes")