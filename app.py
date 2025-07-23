from flask import Flask, render_template, request, flash
import os
from src.logic import run_analysis

app = Flask(__name__)
app.secret_key = 'klklasdfjasdklvxc-masdf'

PROMPTS_DIR = 'prompts'

@app.route('/', methods=['GET', 'POST'])
def index():
    prompt_files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith('.txt')]

    if request.method == 'POST':
        if 'document' not in request.files:
            flash('No file found')
            return render_template('index.html', prompts=prompt_files)
        
        file = request.files['document']

        if file.filename == '':
            flash('No file selected')
            return render_template('index.html', prompts=prompt_files)

        selected_prompt_file = request.form.get('prompt_selection')
        prompt_path = os.path.join(PROMPTS_DIR, selected_prompt_file)
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_text = f.read()

        if file and prompt_text:
            try:
                results = run_analysis(file, prompt_text)
                return render_template('index.html', prompts=prompt_files, results=results)
            except Exception as e:
                flash(f"An error occurred: {e}")

    return render_template('index.html', prompts=prompt_files)

if __name__ == '__main__':
    app.run(debug=True)