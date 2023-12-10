import os
import gradio as gr
import noisereduce as nr
from pydub import AudioSegment
from pedalboard import *
from pedalboard.io import AudioFile
from pathlib import Path

def remove_noise(input_files):
    Path("tmp").mkdir(parents=True, exist_ok=True)
    filelist = [ f for f in os.listdir("tmp") if f.endswith(".mp3") ]
    for f in filelist:
        os.remove(os.path.join("tmp", f))

    processed_files = []
    for input_audio in input_files:
        base_name = os.path.splitext(os.path.basename(input_audio.name))[0]
        output_file = f"{base_name}-processed.mp3"

        samplerate = 44100.0
        with AudioFile(input_audio).resampled_to(samplerate) as f:
            audio = f.read(f.frames)

        reduced_noise = nr.reduce_noise(y=audio, sr=samplerate, stationary=True, prop_decrease=0.75)

        board = Pedalboard([
            NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
            Gain(gain_db=10)
        ])

        effected = board(reduced_noise, samplerate)
        processed_file_path = f'tmp/{output_file}'
        with AudioFile(processed_file_path, 'w', samplerate, effected.shape[0]) as f:
            f.write(effected)

        processed_files.append(processed_file_path)

    return processed_files

with gr.Blocks(title="Noice Reducer Tool") as noiseReductionTool:
   gr.Interface(
       fn=remove_noise,
       inputs=gr.Files(label="Upload MP3 files"),
       outputs=gr.File(label="Processed Audio")
   )

noiseReductionTool.launch()
