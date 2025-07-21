# What does this application do?

- Reads PDF, DOCX, or TXT files and extracts the text, omitting headers and footers.
- Calculates basic word statistics (total, unique, and most frequent words).
- Generates an AI response using OpenAI or Deepseek models via the OpenAI API.
- Saves the generated response to an output file.
- Displays the extracted text, AI response, statistics, and total execution time in the console.

## Libraries used

- openai  
- python-docx  
- PyMuPDF (fitz)  
- pathlib  
- collections (Counter)  
- re  
- textwrap  
- os  
- time  


