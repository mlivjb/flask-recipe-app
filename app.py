from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
SAVE_DIR = "saved_pages"
os.makedirs(SAVE_DIR, exist_ok=True)  # Ensure folder exists

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "Untitled Page")
        ingredients = request.form.get("ingredients", "")
        instructions = request.form.get("instructions", "")
        notes = request.form.get("notes", "")

        # Create a unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SAVE_DIR}/recipe_{title}_{timestamp}.html"

        # Create the full HTML content using a simple template
        with open(filename, "w", encoding="utf-8") as f:
            f.write(render_template("saved_page_template.html", title=title, ingredients=ingredients, instructions=instructions, notes=notes))

        return redirect(url_for('view_saved_pages'))

    return render_template("index.html")

@app.route("/saved")
def view_saved_pages():
    files = os.listdir(SAVE_DIR)
    files.sort(reverse=True)
    return render_template("saved_list.html", files=files)

@app.route("/saved/<filename>")
def load_saved_page(filename):
    return open(os.path.join(SAVE_DIR, filename)).read()
