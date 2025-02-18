from flask import Flask, request, redirect, url_for, render_template
import os
import pyttsx3
import PyPDF2
from gtts import gTTS

app = Flask(__name__)

# Configurar la carpeta de almacenamiento de audios y PDFs
UPLOAD_FOLDER = 'PDFs'
AUDIO_FOLDER = 'AudioRick'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    if 'pdfFile' not in request.files:
        return "No se ha subido ningún archivo."
    
    file = request.files['pdfFile']
    if file.filename == '':
        return "El nombre del archivo es inválido."
    
    if file:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(pdf_path)
        
        # Extraer texto del PDF
        text = extract_text_from_pdf(pdf_path)
        
        if text.strip() == "":
            return "No se pudo extraer texto del PDF."
        
        # Convertir el texto a audio
        audio_filename = file.filename.replace('.pdf', '.mp3')
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        
        convert_text_to_audio(text, audio_path)
        
        # Redirigir a la página de espera mientras se procesa
        return redirect(url_for('esperando'))

@app.route('/esperando')
def esperando():
    return render_template('esperando.html')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

def convert_text_to_audio(text, audio_path):
    tts = gTTS(text, lang='es')
    tts.save(audio_path)

if __name__ == '__main__':
    app.run(debug=True)
