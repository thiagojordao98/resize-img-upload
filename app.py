from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from celery import Celery
import os

app = Flask(__name__)
CORS(app)  

app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/resized_<filename>', methods=['GET'])
def download_resized_image(filename):
    return send_from_directory('', f'resized_{filename}')

@celery.task
def resize_image_task(filename):
    import PIL.Image as Image

    size = (384, 384)

    with Image.open(filename) as img:
        img = img.resize(size)
        img.save(f'resized_{filename}')
    
    os.remove(filename)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    file.save(filename)

    resize_image_task.delay(filename)

    return jsonify({'message': f'File uploaded successfully, processing in background!'}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
