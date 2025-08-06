import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
    RUNTIME_DIR = Path(os.path.dirname(sys.executable))
else:
    BASE_DIR = Path(__file__).parent
    RUNTIME_DIR = BASE_DIR

sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "src"))

os.chdir(BASE_DIR)

config_path = RUNTIME_DIR / "config.ini"
if config_path.exists():
    with open(config_path, "r") as f:
        for line in f:
            if "OPENROUTER_API_KEY" in line:
                key = line.split("=")[1].strip()
                os.environ["OPENROUTER_API_KEY"] = key
                break

from flask import Flask, render_template, request, flash, redirect, url_for
import os
from src.logic import run_analysis, process_folder_batch

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static") if (BASE_DIR / "static").exists() else None,
)

app.secret_key = "secret-bot-kla"
PROMPTS_DIR = str(BASE_DIR / "prompts")


@app.route("/", methods=["GET", "POST"])
def index():
    prompt_files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith(".txt")]

    if request.method == "POST":
        if "document" not in request.files or not request.files["document"].filename:
            flash("No file selected")
            return redirect(url_for("index"))

        file = request.files["document"]
        selected_prompt_file = request.form.get("prompt_selection")
        selected_model = request.form.get("selected_model")
        
        question = request.form.get("question", "").strip()
        theme = request.form.get("theme", "").strip()
        keyword = request.form.get("keyword", "").strip()

        if not selected_model:
            flash("No AI model selected")
            return redirect(url_for("index"))

        prompt_path = os.path.join(PROMPTS_DIR, selected_prompt_file)
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_text = f.read()

        try:
            results = run_analysis(file, prompt_text, selected_model, question, theme, keyword)
            return render_template("index.html", prompts=prompt_files, results=results)
        except Exception as e:
            flash(f"An error occurred during the analysis: {e}")
            return redirect(url_for("index"))

    return render_template("index.html", prompts=prompt_files)


@app.route("/batch", methods=["GET", "POST"])
def batch_process():
    prompt_files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith(".txt")]

    if request.method == "POST":
        folder_path = request.form.get("folder_path")
        output_dir = request.form.get("output_dir")
        file_extension = request.form.get("file_extension")
        selected_prompt_file = request.form.get("prompt_selection")
        selected_model = request.form.get("selected_model")
        
        question = request.form.get("question", "").strip()
        theme = request.form.get("theme", "").strip()
        keyword = request.form.get("keyword", "").strip()

        if not selected_model:
            flash("No AI model selected", "error")
            return redirect(url_for("batch_process"))

        prompt_path = os.path.join(PROMPTS_DIR, selected_prompt_file)
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()

        try:
            flash(
                "Batch process started. Check your terminal for progress updates. Results will appear in your output folder.",
                "success",
            )
            process_folder_batch(
                folder_path, output_dir, file_extension, prompt_template, selected_model, question, theme, keyword
            )
        except Exception as e:
            flash(f"Error starting the process: {e}", "error")

        return redirect(url_for("batch_process"))

    return render_template("batch.html", prompts=prompt_files)
