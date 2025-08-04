import os
import pickle as pkl
from matplotlib import pyplot as plt
import librosa
import soundfile as sf
import numpy as np

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

def load_model(file_name):
    with open(file_name, 'rb') as f:
        return pkl.load(f)

def create_spectrogram(chunk, sr):
    s = librosa.feature.melspectrogram(y=chunk, sr=sr, n_mels=128, fmax=8000)
    s_dB = librosa.power_to_db(s, ref=np.max)
    return s_dB

def extract_features(spectrogram):
    return np.array([spectrogram.flatten()])

def decode_prediction(prediction):
    genre_labels = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    return genre_labels[np.argmax(prediction)]

def predict_genre(spectrogram):
    model = load_model("model.pkl")
    features = extract_features(spectrogram)
    prediction = model.predict(features)
    return decode_prediction(prediction)

model = load_model("model.pkl")
input_path = "./data/song.mp3"
file_name = os.path.splitext(os.path.basename(input_path))[0]
output_path = f"./data/{file_name}_chunks/"
os.makedirs(output_path, exist_ok=True)
os.makedirs(output_path + "spectrograms/", exist_ok=True)

chunks = preprocessing_into_spectrograms(input_path)

for i, (chunk, sr) in enumerate(chunks):
    out_file = os.path.join(output_path, f"{file_name}_chunk_{i}.mp3")
    sf.write(out_file, chunk, sr)

print(f"{len(chunks)} chunks created and saved to {output_path}")

for i, (chunk, sr) in enumerate(chunks):
    spectrogram = create_spectrogram(chunk, sr)
    spectrogram_file = os.path.join(output_path + "spectrograms/", f"{file_name}_chunk_{i}_spectrogram.png")
    plt.imsave(spectrogram_file, spectrogram, cmap='magma')
    print(f"Spectrogram for chunk {i} saved to {spectrogram_file}")
print("Spectrograms created and saved successfully.")

predictions = []
for i in range(len(chunks)):
    spectrogram_file = os.path.join(output_path + "spectrograms/", f"{file_name}_chunk_{i}_spectrogram.png")
    prediction = predict_genre(spectrogram_file)
    predictions.append(prediction)
