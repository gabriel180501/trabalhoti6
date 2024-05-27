import os
import webbrowser
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from threading import Timer
from flask_cors import CORS  # Importe o módulo CORS

app = Flask(__name__)
CORS(app)  # Configure o CORS para permitir solicitações de todas as origens


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            return jsonify({'message': 'File successfully uploaded'}), 200
    except Exception as e:
        return jsonify({'error': f'Error during file upload: {str(e)}'}), 500

@app.route('/')
def index():
    return send_from_directory('static', 'principal.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def open_browser():
    webbrowser.open_new('http://localhost:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()  # Abre o navegador após 1 segundo
    app.run(debug=True, host='0.0.0.0', port=5000)
