from pydub import AudioSegment
from pydub.silence import make_chunks
import librosa
from flask import Flask, request, jsonify
import soundfile as sf
import numpy as np
import os
import matplotlib.pyplot as plt

headers = {
    'Content-Type': 'application/json'
}

def preprocessing_into_spectrograms(file_path, chunk_length_ms=3000):
    y, sr = librosa.load(file_path, sr=None)
    chunk_samples = int((chunk_length_ms / 1000) * sr)
    chunks = []

    for start_sample in range(0, len(y), chunk_samples):
        end_sample = start_sample + chunk_samples
        chunk = y[start_sample:end_sample]
        if len(chunk) < chunk_samples:
            break
        chunks.append((chunk, sr))
    
    return chunks

def predict_genre_from_spectrograms(spectrograms, model):
    predictions = []
    for spectrogram in spectrograms:
        prediction = model.predict(spectrogram)
        predictions.append(prediction)
    return max(set(predictions), key=predictions.count)

def create_spectrogram(chunk, sr):
    s = librosa.feature.melspectrogram(y=chunk, sr=sr, n_mels=128, fmax=8000)
    s_dB = librosa.power_to_db(s, ref=np.max)
    return s_dB

app = Flask(__name__)

@app.route('/clear', methods=['POST'])
def clear():
    for filename in os.listdir("./uploads/"):
        file_path = os.path.join("./uploads/", filename)
        os.remove(file_path)
    return jsonify({'message': 'Uploads cleared successfully'}), 200

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    with open(f"./uploads/{file.filename}", "wb") as f:
        f.write(file.read())
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    return jsonify({'message': 'File uploaded successfully'}, headers), 200

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    model = request.form.get('model')
    if not model:
        return jsonify({'error': 'No model provided'}), 400
    file_path = f"./uploads/{file.filename}"
    file.save(file_path)
    file_name = "./data/song.mp3"
    output_path = f"./data/{file_name}_chunks/"
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(output_path + "spectrograms/", exist_ok=True)
    chunks = preprocessing_into_spectrograms(file_path)
    for i, (chunk, sr) in enumerate(chunks):
        out_file = os.path.join(output_path, f"{file_name}_chunk_{i}.mp3")
        sf.write(out_file, chunk, sr)

    print(f"{len(chunks)} chunks created and saved to {output_path}")

    spectrograms = []
    for i, (chunk, sr) in enumerate(chunks):
        spectrogram = create_spectrogram(chunk, sr)
        spectrogram_file = os.path.join(output_path + "spectrograms/", f"{file_name}_chunk_{i}_spectrogram.png")
        plt.imsave(spectrogram_file, spectrogram, cmap='magma')
        spectrograms.append(spectrogram)
        print(f"Spectrogram for chunk {i} saved to {spectrogram_file}")
    print("Spectrograms created and saved successfully.")

    prediction = predict_genre_from_spectrograms(spectrograms, model)
    
    return jsonify({'message': 'Prediction made successfully', 'prediction': prediction}, headers), 200

@app.route('/uploads', methods=['GET'])
def get_uploads():
    files = os.listdir("./uploads/")
    return jsonify({'uploads': files}), 200

@app.route('/uploads/<filename>', methods=['DELETE'])
def delete_upload(filename):
    file_path = f"./uploads/{filename}"
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'}), 200
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)