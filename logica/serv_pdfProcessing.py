from flask import Flask, request, render_template, send_file
from gtts import gTTS
import PyPDF2
import os

app = Flask(__name__)

# Ruta principal para mostrar el formulario
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el archivo PDF
@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    if 'pdfFile' not in request.files:
        return 'No file part', 400
    file = request.files['pdfFile']
    
    if file.filename == '':
        return 'No selected file', 400

    if file and file.filename.endswith('.pdf'):
        # Leer el contenido del PDF
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Convertir texto a audio
        tts = gTTS(text=text, lang='es')
        audio_path = os.path.abspath("audio.mp3")
        print(f"archivo MPO3 generado en {audio_path}")
        tts.save(audio_path)
        
        # Enviar el archivo de audio generado
        return send_file(audio_path, as_attachment=True)

    return 'Archivo no válido', 400

if __name__ == '__main__':
    app.run(debug=True)
