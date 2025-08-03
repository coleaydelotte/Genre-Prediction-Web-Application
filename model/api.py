from pydub import AudioSegment
from pydub.silence import make_chunks
import librosa
from flask import Flask, request, jsonify

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

app = Flask(__name__)
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
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
    spectrograms = preprocessing_into_spectograms(file_path)
    prediction = predict_genre_from_spectrograms(spectrograms, model)

    return jsonify({'message': 'Prediction made successfully', 'prediction': prediction}, headers), 200

if __name__ == '__main__':
    app.run(debug=True)