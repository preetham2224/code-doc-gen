import os
from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

def generate_doc(code):
    prompt = f"""
    You are a professional code documentation assistant. Analyze the following code and generate a structured documentation covering ONLY the following sections:

    1. Overview
    2. Functionality
    3. Methodology
    4. Technicality
    5. Summary

    Code:
    {code}
    """
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    code = ''
    pasted_code = request.form.get('code')
    uploaded_file = request.files.get('file')

    if pasted_code:
        code = pasted_code.strip()
    elif uploaded_file and uploaded_file.filename.endswith('.py'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        with open(file_path, 'r') as f:
            code = f.read()
    else:
        flash("Please upload a .py file or paste code.")
        return redirect('/')

    documentation = generate_doc(code)
    return render_template('result.html', documentation=documentation)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
