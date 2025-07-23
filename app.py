from flask import Flask, render_template, request, flash, redirect, url_for
import os
from src.logic import run_analysis, process_folder_batch 

app = Flask(__name__)
app.secret_key = 'secret-bot-kla'

PROMPTS_DIR = 'prompts'

@app.route('/', methods=['GET', 'POST'])
def index():
    prompt_files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith('.txt')]

    if request.method == 'POST':
        if 'document' not in request.files or not request.files['document'].filename:
            flash('No file selected')
            return redirect(url_for('index'))

        file = request.files['document']
        selected_prompt_file = request.form.get('prompt_selection')
        prompt_path = os.path.join(PROMPTS_DIR, selected_prompt_file)

        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_text = f.read()

        try:
            results = run_analysis(file, prompt_text)
            return render_template('index.html', prompts=prompt_files, results=results)
        except Exception as e:
            flash(f"An error occurred during the analysis: {e}")
            return redirect(url_for('index'))

    return render_template('index.html', prompts=prompt_files)

@app.route('/batch', methods=['GET', 'POST'])
def batch_process():
    prompt_files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith('.txt')]

    if request.method == 'POST':
        folder_path = request.form.get('folder_path')
        output_dir = request.form.get('output_dir')
        file_extension = request.form.get('file_extension')
        selected_prompt_file = request.form.get('prompt_selection')

        prompt_path = os.path.join(PROMPTS_DIR, selected_prompt_file)
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        try:
            flash("Batch process started. Check your terminal for progress updates. Results will appear in your output folder.", 'success')
            process_folder_batch(folder_path, output_dir, file_extension, prompt_template)
        except Exception as e:
            flash(f"Error starting the process: {e}", 'error')

        return redirect(url_for('batch_process'))

    return render_template('batch.html', prompts=prompt_files)

if __name__ == '__main__':
    app.run(debug=True)