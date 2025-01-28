from flask import Flask, request, render_template, redirect, url_for, session, send_file
from gtts import gTTS
import PyPDF2
import os
import time

app = Flask(__name__, template_folder="paginas")
app.secret_key = 'super_secret_key'  # Necesario para usar `session`

# Crear la carpeta AudioRick si no existe
audio_folder = "AudioRick"
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

# Ruta principal para mostrar el formulario
@app.route('/')
def index():
    return render_template('Selec_work.html')  # Cambiar a tu archivo HTML

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

        if not text.strip():  # Verificar si el texto está vacío
            return "El PDF no contiene texto legible.", 400

        # Convertir texto a audio
        tts = gTTS(text=text, lang='es')

        # Generar un nombre único para el archivo de audio
        audio_file_name = f"audio_{int(time.time())}.mp3"
        audio_path = os.path.join(audio_folder, audio_file_name)
        tts.save(audio_path)
        
        print(f"Archivo MP3 generado en {audio_path}")

        # Guardar el nombre del archivo en la sesión para usarlo después
        session['audio_file'] = audio_path

        # Redirigir a la página de resultado
        return redirect(url_for('resultado'))

    return 'Archivo no válido', 400

# Ruta para mostrar la página de resultado
@app.route('/resultado')
def resultado():
    audio_file = session.get('audio_file')
    if not audio_file or not os.path.exists(audio_file):
        return "Error: No se encontró el archivo de audio.", 400

    return render_template('resultado.html', audio_file=audio_file)

# Ruta para descargar el archivo de audio
@app.route('/descargar_audio')
def descargar_audio():
    audio_file = session.get('audio_file')
    if not audio_file or not os.path.exists(audio_file):
        return "Error: No se encontró el archivo de audio.", 400

    return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
