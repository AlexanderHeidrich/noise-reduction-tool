import os
import gradio as gr
import noisereduce as nr
from pydub import AudioSegment
from pedalboard import *
from pedalboard.io import AudioFile
from pathlib import Path

def remove_noise(input_files, threshold_db, ratio, release_ms, gain):
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
            NoiseGate(threshold_db=threshold_db, ratio=ratio, release_ms=release_ms),
            Gain(gain_db=gain)
        ])

        effected = board(reduced_noise, samplerate)
        processed_file_path = f'tmp/{output_file}'
        with AudioFile(processed_file_path, 'w', samplerate, effected.shape[0]) as f:
            f.write(effected)

        processed_files.append(processed_file_path)

    # todo => how to return list and show list of mp3 files...
    return processed_files

with gr.Blocks(title="Noise Reducer Tool") as noiseReductionTool:
    gr.Interface(
        fn=remove_noise,
        inputs=[
            gr.Files(label="Upload MP3 files"),
            gr.Slider(label="Threshold (dB)", minimum=-60, maximum=0, value=-30),
            gr.Slider(label="Ratio", minimum=1, maximum=10, value=2),
            gr.Slider(label="Release Time (ms)", minimum=10, maximum=500, value=100),
            gr.Slider(label="Gain (dB)", minimum=0, maximum=50, value=10)
        ],
        outputs=[
            gr.File(label="Processed Audio")
        ]
    )

noiseReductionTool.launch()
