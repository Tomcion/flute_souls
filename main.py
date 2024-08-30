import time
import sys
import array

from pydub import AudioSegment
from pydub.utils import get_array_type

from scipy import fft
from scipy.signal import find_peaks

import pyaudio
import matplotlib.pyplot as plt
import numpy as np

from sendKeys import PressKey, ReleaseKey, VK_MENU, VK_TAB
from movements import *

f = open("notes.txt", "w")

SAMPLE_WIDTH = 2
CHANNELS = 2

RECORD_SECONDS = 1000
CHUNK = 1024
RATE = 44100

# MIN_NOTE_VOLUME = -65.0
MIN_NOTE_VOLUME = -22.0

freq_array1 = []
freq_magnitude1 = []
start = time.time()

is_walking = False
is_rotating = False
note_playing = False

def frequency_spectrum(sample, max_frequency=5000):
    """
    Derive frequency spectrum of a pydub.AudioSample
    Returns an array of frequencies and an array of how prevalent that frequency is in the sample
    """
    
    # Convert pydub.AudioSample to raw audio data
    # Copied from Jiaaro's answer on https://stackoverflow.com/questions/32373996/pydub-raw-audio-data
    bit_depth = sample.sample_width * 8
    array_type = get_array_type(bit_depth)
    raw_audio_data = array.array(array_type, sample._data)
    n = len(raw_audio_data)
    # Compute FFT and frequency value for each index in FFT array
    # Inspired by Reveille's answer on https://stackoverflow.com/questions/53308674/audio-frequencies-in-python
    freq_array = np.arange(n) * (float(sample.frame_rate) / n)  # two sides frequency range
    freq_array = freq_array[:(n // 2)]  # one side frequency range
    raw_audio_data = raw_audio_data - np.average(raw_audio_data)  # zero-centering
    
    freq_magnitude = fft.fft(raw_audio_data) # fft computing and normalization
    freq_magnitude = freq_magnitude[:(n // 2)] # one side
    if max_frequency:
        max_index = int(max_frequency * n / sample.frame_rate) + 1
        freq_array = freq_array[:max_index]
        freq_magnitude = freq_magnitude[:max_index]
    freq_magnitude = abs(freq_magnitude)
    freq_magnitude = freq_magnitude / np.sum(freq_magnitude)
    return freq_array, freq_magnitude

def callback(bytes, frame_count, time_info, status):
    # global freq_array1
    # global freq_magnitude1
    global note_playing
    global is_walking
    global is_rotating

    sound = AudioSegment(
        data=bytes,
        sample_width=SAMPLE_WIDTH,
        frame_rate=RATE,
        channels=CHANNELS    
    )
    # .high_pass_filter(100).low_pass_filter(10000)

    # print(sound.dBFS)

    if sound.dBFS > MIN_NOTE_VOLUME:
        # print(sound.dBFS)
        freq_array, freq_magnitude = frequency_spectrum(sound)
        # print(freq_array)
        peak_indicies, props = find_peaks(freq_magnitude, height=0.01)
        heights = props["peak_heights"]
        sorted_indicies = [
            x for (y, x) in sorted(
                zip(heights, peak_indicies),
                key=lambda pair: pair[0],
                reverse=True
            )
        ]
        sorted_heights = sorted(heights, reverse=True)
        freq_index = sorted_indicies[0]

        # line = ""
        # for i, peak in enumerate(sorted_indicies):
        #     freq = freq_array[peak]
        #     magnitude = sorted_heights[i]
        #     line += str(peak) + "    "
        # line += "\n"
        # print(line)

        note = ""
        # if freq_index == 7 or freq_index == 13 or freq_index == 13:
        if freq_index == 7:
            note = "C1"
        elif freq_index == 8:
            note = "D1"
        elif freq_index == 9:
            note = "F1"
        elif freq_index == 10:
            note = "G1"
        elif freq_index == 11 or freq_index == 12:
            note = "A1"
        elif freq_index == 13 or freq_index == 14:
            if 7 in sorted_indicies:
                note = "C1"
            else:
                note = "C2"
        elif freq_index == 15:
            note = "E2"
        elif freq_index == 16:
            note = "D#2"

        if note != "" and not note_playing:
            note_playing = True
            print(note)
            if is_walking == True and not note in ("C1", "D1"):
                is_walking = False
                stopWalkForward()
                # print("stop walk")
            elif note == "G1" and not is_walking:
                is_walking = True
                walkForward()
                # print("start walk")

            if note == "C1":
                rotateRight()
                is_rotating = True
            elif note == "D1":
                rotateLeft()
                is_rotating = True
            elif note == "F1":
                heal()
            elif note == "A1":
                roll()
            elif note == "C2":
                lockOn()
            elif note == "E2":
                attack()
            elif note == "D#2":
                collect()
        elif note == "" and note_playing:
            note_playing = False
            # print("atonal")
        
        print(note)


    else:
        if note_playing:
            note_playing = False
            if is_rotating:
                is_rotating = False
                stopRotate()
            # print("silent")

    return (bytes, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(SAMPLE_WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)

start = time.time()
# while stream.is_active() and (time.time() - start) < RECORD_SECONDS:
while stream.is_active():
    time.sleep(0.1)

stream.close()
p.terminate()
f.close()
