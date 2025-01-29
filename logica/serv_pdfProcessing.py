import os
import time
import threading
from flask import Flask, request, render_template, redirect, url_for, session, send_file
from gtts import gTTS
import PyPDF2

# Obtener la ruta base del proyecto
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Configurar Flask para buscar las páginas en "paginas/"
app = Flask(__name__, template_folder=os.path.join(base_dir, "paginas"))
app.secret_key = 'super_secret_key'

# Crear carpetas necesarias
audio_folder = os.path.join(base_dir, "AudioRick")
pdf_folder = os.path.join(base_dir, "PDFs")

if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

# Página principal
@app.route('/')
def index():
    return render_template('Selec_work.html')

# Página de espera
@app.route('/esperando')
def esperando():
    return render_template('esperando.html')

# Procesar PDF en un hilo
def process_pdf(pdf_path, session_id):
    try:
        # Leer el PDF
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''.join([page.extract_text() or '' for page in pdf_reader.pages])

        if not text.strip():
            session[f'error_{session_id}'] = "El PDF no contiene texto legible."
            return

        # Convertir a audio
        tts = gTTS(text=text, lang='es')
        audio_file_name = f"audio_{int(time.time())}.mp3"
        audio_path = os.path.join(audio_folder, audio_file_name)
        tts.save(audio_path)

        # Guardar en la sesión
        session[f'audio_file_{session_id}'] = audio_file_name

    except Exception as e:
        session[f'error_{session_id}'] = f"Error al procesar el PDF: {str(e)}"

# Subir PDF y procesarlo
@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    if 'pdfFile' not in request.files:
        return 'No file part', 400

    file = request.files['pdfFile']
    
    if file.filename == '':
        return 'No selected file', 400

    if file and file.filename.endswith('.pdf'):
        # Guardar el archivo en una ubicación temporal
        pdf_path = os.path.join(pdf_folder, f"temp_{int(time.time())}.pdf")
        file.save(pdf_path)

        # Crear un identificador único para la sesión
        session_id = str(time.time())
        session['session_id'] = session_id

        # Ejecutar en un hilo separado
        thread = threading.Thread(target=process_pdf, args=(pdf_path, session_id))
        thread.start()

        return redirect(url_for('esperando'))

    return 'Archivo no válido', 400

# Página de resultado
@app.route('/resultado')
def resultado():
    session_id = session.get('session_id')
    if not session_id:
        return "Error: Sesión no encontrada.", 400

    audio_file = session.get(f'audio_file_{session_id}')
    if not audio_file:
        error_msg = session.get(f'error_{session_id}', "Error desconocido.")
        return f"Error: {error_msg}", 400

    return render_template('resultado.html', audio_file=url_for('static', filename=f'AudioRick/{audio_file}'))

# Descargar audio
@app.route('/descargar_audio')
def descargar_audio():
    session_id = session.get('session_id')
    if not session_id:
        return "Error: Sesión no encontrada.", 400

    audio_file = session.get(f'audio_file_{session_id}')
    if not audio_file:
        return "Error: No se encontró el archivo de audio.", 400

    audio_path = os.path.join(audio_folder, audio_file)
    if not os.path.exists(audio_path):
        return "Error: El archivo de audio ya no está disponible.", 400

    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
