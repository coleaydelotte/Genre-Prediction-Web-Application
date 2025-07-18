from pydub import AudioSegment
from pydub.silence import make_chunks

def split_audio_file(file_path, chunk_length=3000):
    audio = AudioSegment.from_file(file_path)
    chunks = make_chunks(audio, chunk_length)
    return chunks