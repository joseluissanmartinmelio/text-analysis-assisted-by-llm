import os
import textwrap
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