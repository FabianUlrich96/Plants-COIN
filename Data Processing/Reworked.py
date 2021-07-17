from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import pandas as pd
import datetime
import glob
import librosa
import librosa.display
from scipy import signal
import os

def transform_data(data, samplerate):
    length = int(len(data) / samplerate)
    print(length)
    start = 0
    finish = samplerate
    new_data = np.array([])
    while start < len(data):
        data_new = data[start:finish]
        snippet_mean = np.mean(data_new)
        new_data = np.append(new_data, [snippet_mean])
        start = start + samplerate
        finish = finish + samplerate

    transformed_data = new_data[0:len(new_data) - 1]

    return transformed_data, length

def butter_function(data, samplerate):
    nyq = 0.5 * samplerate
    low_cut = 0
    high_cut = 20
    low = low_cut / nyq
    high = high_cut / nyq

    b, a = signal.butter(20, 0.1, 'low')
    filteredData = signal.filtfilt(b, a, data)  # data is the signal to be filtered

    return filteredData



def plot_line_chart(decibel_file, data, title):
    fig, host = plt.subplots(figsize=(8, 5))  # (width, height) in inches

    i = 0
    x = np.array([])
    while i < len(data):
        x = np.append(x, [i])
        i = i + 1

    par1 = host.twinx()
    par2 = host.twinx()

    txt = title
    host.set_title(txt)
    host.set_xticks(x, minor=False)
    #host.set_xticklabels(time, fontdict=None, minor=False, rotation=90)

    temp = host.get_xticklabels()
    temp = list(set(temp) - set(temp[::4]))
    for label in temp:
        label.set_visible(False)
    color1 = colors.cnames['green']
    color2 = colors.cnames['red']
    color3 = colors.cnames['orange']
    host.set_xlabel("Time")

    host.set_ylabel("Amplitude", color=color1)

    par2.spines['right'].set_position(('outward', 60))
    p1, = host.plot(data, color=color1)
    par1.set_ylabel('Decibel', color=color2)
    p2, = par1.plot(decibel_file, color=color2)
    
    plt.show()

    return txt


def my_print(data):
    # maximalwert
    print('Maximum:', np.amax(data))
    # minimalwert
    print('Minimum:', np.amin(data))
    # differenz zwischen minimum und maximum
    print('Amplitude:', np.ptp(data))
    # median
    print('Median:', np.median(data))
    # durchschnittlicher wert
    print('Durchschnitt:', np.mean(data))


def fft_function(data, sample_rate, title):
    # https://pythontic.com/visualization/signals/fouriertransform_fft
    # fast furiour transform is an implementation of discrete fourier transform,
    # which converts a finite sequence into a same-length discrete time fourier transform, which is a function of frequency
    fft = np.fft.fft(data) / len(data)  # Normalize amplitude

    fft = fft[range(int(len(data) / 2))]  # Exclude sampling frequency
    length = len(data)
    values = np.arange(int(length / 2))
    time_period = length/sample_rate
    frequencies = values/time_period
    # https://www.fluke.com/en/learn/blog/electrical/what-is-frequency
    # Frequency is the rate at which current changes direction per second. It is measured in hertz (Hz)
    plt.plot(frequencies, abs(fft))
    plt.title(title + "Frequency(Hz)")
    plt.xlim(right=10)
    plt.xlim(left=0)
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")

    plt.show()
    
def melplot(path):
    data, sample_rate = librosa.load(path)
    T = librosa.feature.melspectrogram(data, sr=sample_rate)
    Tconv = librosa.power_to_db(T)
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Tconv, sr=sample_rate, x_axis='time', y_axis='hz')
    plt.title("MFCC"+path)
    plt.colorbar()
    plt.show()

def main():
    PATH = './Data-Split/' # Use your path
    PATHDECIBEL = './Data-Split/Decibel/'

### Fetch all files in path
    fileNames = os.listdir(PATH)
    fileNamesDecibel = os.listdir(PATHDECIBEL)
    print(fileNames[0])
    print(len(fileNamesDecibel))
### Filter file name list for files ending with .csv
    fileNames = [file for file in fileNames if '.wav' in file]
    fileNamesDecibel = [file for file in fileNamesDecibel if '.csv' in file]
    i=0
    while i < len(fileNames):
        samplerate, data = wavfile.read(PATH + fileNames[i])
        transformed_data, length = transform_data(data, samplerate)
        #filtered_signal = butter_function(transformed_data, samplerate)
        d = pd.read_csv(PATHDECIBEL + fileNamesDecibel[i])
        melplot(PATH + fileNames[i])
        title = plot_line_chart(d, transformed_data, fileNames[i])
        i+=1



if __name__ == '__main__':
    main()
