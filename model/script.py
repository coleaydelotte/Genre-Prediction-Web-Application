import os

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

def create_spectrogram(chunk, sr):
    S = librosa.feature.melspectrogram(y=chunk, sr=sr, n_mels=128, fmax=8000)
    S_dB = librosa.power_to_db(S, ref=np.max)
    return S_dB

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
    plt.imsave(spectrogram_file, spectrogram, cmap='viridis')
    print(f"Spectrogram for chunk {i} saved to {spectrogram_file}")
print("Spectrograms created and saved successfully.")