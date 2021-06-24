from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
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
    wav_file = "." + user_input
    start_time = (user_input[-12:-4])
    start_time = start_time.replace(".", ":")
    return wav_file, decibel_file, start_time


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


def my_print(decibel_file, data, time):
    txt = input("Enter a graph name:")
    i = 0
    x = np.array([])
    while i < len(data):
        x = np.append(x, [i])
        i = i + 1

    print(x)
    plt.figure(txt)
    plt.title(txt)
    plt.xticks(x, time, rotation='vertical')
    plt.plot(data)
    ax1 = plt.gca()
    temp = ax1.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::4]))
    for label in temp:
        label.set_visible(False)

    color = colors.cnames['green']

    plt.ylabel("Amplitude")
    plt.xlabel("Time")
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
    # print(numpy.average(data))
    # limit x
    # plt.xlim(0, 10000)
    while len(decibel_file) is not len(data):
        decibel_file = np.insert(decibel_file, 1, 0, axis=0)
    ax2 = ax1.twinx()
    ax2.plot(decibel_file, color=color)
    ax2.set_ylabel("dB", color=color)

    plt.show()


# myprint(samplerate, data, plant+"_no_sound")
# myprint(sampleratet1, datat1, plant+"_traffic1")
# myprint(sampleratet2, datat2, plant+"_traffic2")
# myprint(sampleratet3, datat3, plant+"_traffic3")
# myprint(sampleratec1, datac1, plant+"_con1")
# myprint(sampleratec2, datac2, plant+"_con2")
# myprint(sampleratec3, datac3, plant+"_con3")


def main():
    wav_file, decibel_file, start_time = select_file()
    samplerate, data = wavfile.read(wav_file)
    decibel_file = np.genfromtxt('.' + decibel_file, delimiter=',', skip_header=1)
    print("Länge:")
    print(len(decibel_file))
    transformed_data, length = transform_data(data, samplerate)
    time_labels = create_labels(length, start_time)
    my_print(decibel_file, transformed_data, time_labels)


if __name__ == '__main__':
    main()
