from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from src.logic import run_analysis, process_folder_batch, unify_markdowns_and_create_pdf

app = Flask(__name__)
app.secret_key = "secret-bot-kla"

PROMPTS_DIR = "prompts"


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


@app.route("/unify-markdowns", methods=["POST"])
def unify_markdowns():
    """
    Endpoint para unificar archivos markdown de un directorio en un solo archivo y generar PDF
    """
    try:
        data = request.get_json()
        output_dir = data.get("output_dir")
        
        if not output_dir:
            return jsonify({
                "success": False, 
                "message": "No output directory specified"
            }), 400
        
        result = unify_markdowns_and_create_pdf(output_dir)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error during unification: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
