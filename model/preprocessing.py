from pydub import AudioSegment
from pydub.silence import make_chunks
import librosa

def preprocessing_into_spectograms(file_path, chunk_length=3000):
    audio = AudioSegment.from_file(file_path)
    chunks = make_chunks(audio, chunk_length)
    spectrograms = []
    for _, chunk in enumerate(chunks):
        mel_spectrogram = librosa.feature.melspectrogram(y=chunk.get_array_of_samples(), sr=chunk.frame_rate)
        spectrograms.append(mel_spectrogram)
    return spectrograms

def predict_genre_from_spectrograms(spectrograms, model):
    predictions = []
    for spectrogram in spectrograms:
        prediction = model.predict(spectrogram)
        predictions.append(prediction)
    return max(set(predictions), key=predictions.count)