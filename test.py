import wave
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

SAMPLE_WIDTH = 2
CHANNELS = 2

RECORD_SECONDS = 1000
CHUNK = 1024
RATE = 44100

MIN_NOTE_VOLUME = -22.0

freq_array = []
freq_magnitude = []

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

with wave.open('clip.wav', 'rb') as wf:
    def callback(bytes, frame_count, time_info, status):
        global freq_array
        global freq_magnitude
        data = wf.readframes(frame_count)

        sound = AudioSegment(
            data=data,
            sample_width=wf.getsampwidth(),
            frame_rate=wf.getframerate(),
            channels=wf.getnchannels()    
        )
        # .high_pass_filter(100).low_pass_filter(10000)

        if sound.dBFS > MIN_NOTE_VOLUME:
            print(sound.dBFS)
            freq_array, freq_magnitude = frequency_spectrum(sound)
            peak_indicies, props = find_peaks(freq_magnitude, height=0.015)
            heights = props["peak_heights"]
            sorted_indicies = [
                x for (y, x) in sorted(
                    zip(heights, peak_indicies),
                    key=lambda pair: pair[0],
                    reverse=True
                )
            ]
            print(heights)
            sorted_heights = sorted(heights, reverse=True)
            print(sorted_heights)
            for i, peak in enumerate(sorted_indicies):
                if i >= 3:
                    break
                freq = freq_array[peak]
                magnitude = heights[i]
                print("{}hz with magnitude {:.3f}".format(freq, magnitude))
            # return (bytes, pyaudio.paComplete)

        return (data, pyaudio.paContinue)

    while True:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)

        start = time.time()
        # while stream.is_active() and (time.time() - start) < RECORD_SECONDS:
        while stream.is_active():
            time.sleep(0.1)

        # plt.plot(freq_array, freq_magnitude, 'b')
        # plt.show()

        stream.close()
        p.terminate()


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