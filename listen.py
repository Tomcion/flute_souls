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

MIN_NOTE_VOLUME = -15.0

freq_array1 = []
freq_magnitude1 = []

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

    if sound.dBFS > MIN_NOTE_VOLUME:
        print(sound.dBFS)
        freq_array, freq_magnitude = frequency_spectrum(sound)
        peak_indicies, props = find_peaks(freq_magnitude, height=0.015)
        # print(freq_array)
        # print(freq_array[peak_indicies[0]], props["peak_heights"][0])
        # print(freq_array[peak_indicies[1]], props["peak_heights"][1])
        # print(freq_array[peak_indicies[2]], props["peak_heights"][2])
        note = peak_indicies[0]
        if note == 7:
            PressKey(0x57) # w
            time.sleep(0.1)    
            ReleaseKey(0x57)
        if note == 10:
            PressKey(0x53) # s
            time.sleep(0.1)    
            ReleaseKey(0x53)
        if note == 8:
            PressKey(0x41) # a
            time.sleep(0.1)    
            ReleaseKey(0x41)
        if note == 9:
            PressKey(0x44) # d
            time.sleep(0.1)    
            ReleaseKey(0x44)
        for i, peak in enumerate(peak_indicies):
            freq = freq_array[peak]
            magnitude = props["peak_heights"][i]
            print("{}hz with magnitude {:.3f}".format(freq, magnitude))
        return (bytes, pyaudio.paComplete)

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
