from pydub import AudioSegment
from pydub.silence import make_chunks
import librosa

def preprocessing_into_spectograms(file_path, chunk_length=3000):
    audio = AudioSegment.from_file(file_path)
    chunks = make_chunks(audio, chunk_length)
    spectograms = []
    for _, chunk in enumerate(chunks):
        mel_spectrogram = librosa.feature.melspectrogram(y=chunk.get_array_of_samples(), sr=chunk.frame_rate)
        spectograms.append(mel_spectrogram)
    return spectograms