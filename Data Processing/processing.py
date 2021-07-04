from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import pandas as pd
import datetime
import glob


# samplerate, data = wavfile.read("./Data/Big-Mimosa/bm_no_sound.wav")
# plant = "Mini-Mimosa"
# plant = "Big-Mimosa"
# plant = "Basil"
# plant = "Chili"
# samplerate, data = wavfile.read("./Data/" + plant + "/no_sound-16.35.30.wav")
# sampleratet1, datat1 = wavfile.read("./Data/" + plant + "/traffic1.wav")
# sampleratet2, datat2 = wavfile.read("./Data/" + plant + "/traffic2.wav")
# sampleratet3, datat3 = wavfile.read("./Data/" + plant + "/traffic3.wav")
# sampleratec1, datac1 = wavfile.read("./Data/" + plant + "/con1.wav")
# sampleratec2, datac2 = wavfile.read("./Data/" + plant + "/con2.wav")
# sampleratec3, datac3 = wavfile.read("./Data/" + plant + "/con3.wav")


# samplerate, data = wavfile.read("./Data/Big-Mimosa/bm_no_sound.wav")
# samplerate, data = wavfile.read("./Data/Big-Mimosa/bm_no_sound.wav")


def select_file():
    user_input = ""
    while not user_input.endswith(".wav"):
        print(glob.glob("." + user_input + "/*"))
        user_input = user_input + "/" + input("Choose a Directory:")
        wav_directory = glob.glob("./" + user_input + "/*.wav")

        print(user_input)
        if bool(wav_directory):
            print(glob.glob("./" + user_input + "/*.wav"))
            user_input = user_input + "/" + input("Choose a File:")

    decibel_file = user_input[:-4] + "_decibel.csv"
    sensor_file = user_input[:-4] + ".csv"
    wav_file = "." + user_input
    start_time = (user_input[-12:-4])
    start_time = start_time.replace(".", ":")
    return wav_file, decibel_file, sensor_file, start_time


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


def create_labels(length, start_time):
    d = datetime.datetime.strptime(start_time, '%H:%M:%S').time()

    time_array = np.array([])
    for i in range(length):
        time = (datetime.datetime.combine(datetime.date(1, 1, 1), d) + datetime.timedelta(seconds=i)).time()
        time = time.strftime('%H:%M:%S')
        time_array = np.append(time_array, [time])

    time_labels = time_array

    return time_labels


def select_values():
    values = ["Decibel", "Photoresistor", "Humidity", "Temperature", "CO2", "Soil_Moisture", "Nothing"]
    value1 = None
    while value1 not in values:
        print("Please enter a first value from the list: ")
        print(values)
        value1 = input("Input:")

    value2 = None
    while value2 not in values:
        print("Please enter a second value from the list: ")
        print(values)
        value2 = input("Input:")

    print("Thank you!")

    return value1, value2


def plot_line_chart(value1, value2, decibel_file, sensor_file, data, time):
    fig, host = plt.subplots(figsize=(8, 5))  # (width, height) in inches

    i = 0
    x = np.array([])
    while i < len(data):
        x = np.append(x, [i])
        i = i + 1

    par1 = host.twinx()
    par2 = host.twinx()

    txt = input("Enter a graph name:")
    host.set_title(txt)
    host.set_xticks(x, minor=False)
    host.set_xticklabels(time, fontdict=None, minor=False, rotation=90)

    temp = host.get_xticklabels()
    temp = list(set(temp) - set(temp[::4]))
    for label in temp:
        label.set_visible(False)
    color1 = colors.cnames['green']
    color2 = colors.cnames['red']
    color3 = colors.cnames['orange']
    host.set_xlabel("Time")

    host.set_ylabel("Amplitude", color=color1)

    if value1 == "Decibel":
        file1 = decibel_file
    else:
        file1 = sensor_file

    if value2 == "Decibel":
        file2 = decibel_file
    else:
        file2 = sensor_file

    par2.spines['right'].set_position(('outward', 60))
    p1, = host.plot(data, color=color1)
    if value1 == "Nothing":

        pass
    else:
        par1.set_ylabel(value1, color=color2)
        p2, = par1.plot(file1[value1], color=color2)
    if value2 == "Nothing":
        pass
    else:
        p3, = par2.plot(file2[value2], color=color3)
        par2.set_ylabel(value2, color=color3)

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


def main():
    value1, value2 = select_values()
    wav_file, decibel_file, sensor_file, start_time = select_file()
    samplerate, data = wavfile.read(wav_file)
    decibel_file = pd.read_csv('.' + decibel_file)
    sensor_file = pd.read_csv('.' + sensor_file)
    transformed_data, length = transform_data(data, samplerate)
    time_labels = create_labels(length, start_time)
    title = plot_line_chart(value1, value2, decibel_file, sensor_file, transformed_data, time_labels)

    fft_function(data, samplerate, title)


if __name__ == '__main__':
    main()
