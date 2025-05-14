from pydub import AudioSegment
from pydub.playback import play

def play_sound(file_path: str):
    sound = AudioSegment.from_file(file_path)
    play(sound)