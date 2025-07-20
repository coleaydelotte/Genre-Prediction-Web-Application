import flask
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    return jsonify({'message': 'File uploaded successfully'}), 200
