# This file uses the microphone to listen.
# requires pyaudio:
# http://people.csail.mit.edu/hubert/pyaudio/
# pip install pyaudio

import pyaudio
import wave
import os

#Need to write a temporary file.

# Default recording values.
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
WAVE_OUTPUT_DIR = "tmp"
WAVE_OUTPUT_FILENAME = "output.wav"
WAVE_OUTPUT_PATH = os.path.join(WAVE_OUTPUT_DIR, WAVE_OUTPUT_FILENAME)


def record_file(rate=44100, record_seconds=10, wave_output_filename=WAVE_OUTPUT_PATH):
    if not os.path.exists(WAVE_OUTPUT_DIR):
        os.makedirs(WAVE_OUTPUT_DIR)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=rate,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(rate / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(wave_output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    print("hello")
    record_file()