from TeraTTS import TTS
from fileToText import convert_file_to_text
import os

def text_to_speech(text, output_file):
    tts = TTS("TeraTTS/girl_nice-g2p-vits", add_time_to_end=1.0, tokenizer_load_dict=True)
    audio = tts(text, lenght_scale=1.2)
    tts.save_wav(audio, output_file)

def convert_file_to_speech(file_path):
    text = convert_file_to_text(file_path)
    if text is not None:
        output_file = os.path.splitext(file_path)[0] + '.wav'
        text_to_speech(text, output_file)
