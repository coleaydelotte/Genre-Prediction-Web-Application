import os
import librosa
import soundfile as sf

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

input_path = "./data/song.mp3"
file_name = os.path.splitext(os.path.basename(input_path))[0]
output_path = f"./data/{file_name}_chunks/"
os.makedirs(output_path, exist_ok=True)

chunks = preprocessing_into_spectrograms(input_path)

for i, (chunk, sr) in enumerate(chunks):
    out_file = os.path.join(output_path, f"{file_name}_chunk_{i}.wav")
    sf.write(out_file, chunk, sr)

print(f"{len(chunks)} chunks created and saved to {output_path}")
