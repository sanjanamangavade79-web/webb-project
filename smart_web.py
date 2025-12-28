from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def summarize_text(text, keywords):
    lines = text.split("\n")

    summary_lines = [line for line in lines if any(word in line for word in keywords)]
    return "".join(summary_lines)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    summary = ""
    if request.method == 'POST':

        file = request.files['file']
        keywords = request.form['keywords'].split(",")
        if file:
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8' ,errors='ignore') as f:

                file_text = f.read()
            summary = summarize_text(file_text, keywords)
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)