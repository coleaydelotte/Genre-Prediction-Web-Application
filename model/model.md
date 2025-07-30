# Aydelotte Classifier
using the Aydelotte classifier to ensure accuracy
### Must find data to train on
- GTZAN is a good start but going to be issue because we must be able to derive the data from a link or song.
- sample data in file named `sample_data.csv`

    spectrograms = []
    for _, chunk in enumerate(chunks):
        mel_spectrogram = librosa.feature.melspectrogram(y=chunk.get_array_of_samples(), sr=chunk.frame_rate)
        spectrograms.append(mel_spectrogram)
    return spectrograms