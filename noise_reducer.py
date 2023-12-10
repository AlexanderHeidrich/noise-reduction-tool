import gradio as gr
from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import os
from pedalboard import *
from pedalboard.io import AudioFile

from pathlib import Path

def remove_noise(input_audio):
   Path("tmp").mkdir(parents=True, exist_ok=True)

   base_name = os.path.splitext(os.path.basename(input_audio.name))[0]
   output_file = f"{base_name}_processed.mp3"

   samplerate = 44100.0
   with AudioFile(input_audio).resampled_to(samplerate) as f:
    audio = f.read(f.frames)

   reduced_noise = nr.reduce_noise(y=audio, sr=samplerate, stationary=True, prop_decrease=0.75)

   board = Pedalboard([
       NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
       Compressor(threshold_db=-16, ratio=2.5),
       LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
       Gain(gain_db=10)
   ])

   effected = board(reduced_noise, samplerate)
   with AudioFile('tmp/' + output_file, 'w', samplerate, effected.shape[0]) as f:
     f.write(effected)

   return 'tmp/' + output_file

iface = gr.Interface(
    fn=remove_noise,
    inputs=gr.File(label="Upload an MP3 file"),
    outputs=gr.File(label="Processed Audio")
)

iface.launch()
