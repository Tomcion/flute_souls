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

MIN_NOTE_VOLUME = -65.0
# MIN_NOTE_VOLUME = -22.0

freq_array1 = []
freq_magnitude1 = []
start = time.time()

is_walking = False
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

    sound = AudioSegment(
        data=bytes,
        sample_width=SAMPLE_WIDTH,
        frame_rate=RATE,
        channels=CHANNELS    
    )
    # .high_pass_filter(100).low_pass_filter(10000)

    # print(sound.dBFS)
    note_playing = False

    if sound.dBFS > MIN_NOTE_VOLUME:
        # print(sound.dBFS)
        freq_array, freq_magnitude = frequency_spectrum(sound)
        # print(freq_array)
        peak_indicies, props = find_peaks(freq_magnitude, height=0.015)
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
        note = ""
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
            if freq_index == 14 and 7 in sorted_indicies:
                note = "C1"
            else:
                note = "C2"
        elif freq_index == 15:
            note = "E2"
        elif freq_index == 16:
            note = "D#2"

        if note == "":
            note_playing = False
        else:
            note_playing = True
        
        print(note)
        line = ""
        for i, peak in enumerate(sorted_indicies):
            freq = freq_array[peak]
            magnitude = sorted_heights[i]
            line += str(peak) + "    "

        line += "\n"
        # print(line)
        # if note == "A1" and not is_walking:
        #     is_walking = True
        #     walkForward()
        # elif note == "A1":
        #     is_walking = False

        if note == "C1":
            rotateRight(CHUNK / RATE)
        elif note == "D1":
            rotateLeft(CHUNK / RATE)
        # elif note == "F1":
        #     heal()
        # elif note == "G1":
        #     roll()
        # elif note == "C2":
        #     attack()
        # elif note == "E2":
        #     lockOn()
        # elif note == "D#2":
        #     collect()

        # f.write(line)
        # print(start)
        # print(time.time())
        # print(start - time.time())
        # if time.time() - start >= 20:
        #     return (bytes, pyaudio.paComplete)

    # if sound.dBFS > MIN_NOTE_VOLUME:
    #     print(sound.dBFS)
    #     freq_array, freq_magnitude = frequency_spectrum(sound)
    #     peak_indicies, props = find_peaks(freq_magnitude, height=0.015)
    #     # print(freq_array)
    #     # print(freq_array[peak_indicies[0]], props["peak_heights"][0])
    #     # print(freq_array[peak_indicies[1]], props["peak_heights"][1])
    #     # print(freq_array[peak_indicies[2]], props["peak_heights"][2])
    #     note = peak_indicies[0]
    #     if note == 7:
    #         PressKey(0x57) # w
    #         # time.sleep(0.1)    
    #         ReleaseKey(0x57)
    #     if note == 10:
    #         PressKey(0x53) # s
    #         # time.sleep(0.1)    
    #         ReleaseKey(0x53)
    #     if note == 8:
    #         PressKey(0x41) # a
    #         # time.sleep(0.1)    
    #         ReleaseKey(0x41)
    #     if note == 9:
    #         PressKey(0x44) # d
    #         # time.sleep(0.1)    
    #         ReleaseKey(0x44)
    #     for i, peak in enumerate(peak_indicies):
    #         freq = freq_array[peak]
    #         magnitude = props["peak_heights"][i]
    #         print("{}hz with magnitude {:.3f}".format(freq, magnitude))
    #     # return (bytes, pyaudio.paComplete)
    print(note_playing)
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


# while True:
#     p = pyaudio.PyAudio()
#     stream = p.open(format=p.get_format_from_width(SAMPLE_WIDTH),
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     output=False,
#                     stream_callback=callback)

#     start = time.time()
#     while stream.is_active() and (time.time() - start) < RECORD_SECONDS:
#         time.sleep(0.1)

#     plt.plot(freq_array1, freq_magnitude1, 'b')
#     plt.show()

#     stream.close()
#     p.terminate()
