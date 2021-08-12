from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import pandas as pd
import datetime
import glob
import librosa
import librosa.display
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.stats as scst
import numpy as np


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



def main():
##    samplerate1, data1 = wavfile.read('./Data4/Chili/chili_construction1_old.wav')
##    samplerate2, data2 = wavfile.read('./Data4/Chili/chili_construction2_old.wav')
##    samplerate3, data3 = wavfile.read('./Data4/Chili/chili_construction3_old.wav')
##    samplerate4, data4 = wavfile.read('./Data4/chili_construction_new.wav')
    samplerate1, data1 = wavfile.read('./Data4/Chili/chili_nosound_old.wav')
    #samplerate2, data2 = wavfile.read('./Data4/Chili/chili_construction2_old.wav')
    #samplerate3, data3 = wavfile.read('./Data4/Chili/chili_construction3_old.wav')
    samplerate4, data4 = wavfile.read('./Data4/Chili_nosound_new.wav')
    print(data1, samplerate1)
    #print(data2, samplerate2)
    a, length1 = transform_data(data1, samplerate1)    
    #b, length2 = transform_data(data2, samplerate2)
    #c, length3 = transform_data(data3, samplerate3)
    d, length4 = transform_data(data4, samplerate4)
    #e = np.append(a, b, axis=0)
    #f = np.append(e, c, axis=0)
    print(a,d)
    #f = np.stack(a,b,c)
    #print(f)
    #print(length1, length2, length3, f.size)
    print('----------------------------')
    #print(a,b)
    print(scst.ttest_ind(a,d))

if __name__ == '__main__':
    main()
