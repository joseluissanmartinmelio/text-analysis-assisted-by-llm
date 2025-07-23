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
- flask

## Sources used for create this project

- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Styling_web_forms
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Advanced_form_styling
- https://realpython.com/html-css-python/
- https://realpython.com/python-web-applications/
- https://j2logo.com/tutorial-flask-espanol/
- AI assistant with a local [Deepseek-r1:14b](https://ollama.com/library/deepseek-r1:14b) model powered by RTX 4070 Ti SUPER