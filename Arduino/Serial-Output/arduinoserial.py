import serial
import audioop
import pyaudio
import math
from datetime import datetime
import numpy as np
import pandas as pd
import subprocess
import time
import pyautogui

spike_recorder_path = "C:\Program Files (x86)/Backyard Brains/Spike Recorder/SpikeRecorder.exe"
SAMPLING_RATE = 22050
NUM_SAMPLES = 2048


def start_spikerbox():
    subprocess.Popen(spike_recorder_path)
    time.sleep(3)
    pyautogui.click(752, 271, duration=0.25)
    pyautogui.click(1273, 271, duration=0.25)


def stop_spikerbox():
    pyautogui.click(1325, 302)


def decibel_recording(decibel_array):
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=2, rate=SAMPLING_RATE,
                     input=True, frames_per_buffer=NUM_SAMPLES)

    data = stream.read(NUM_SAMPLES)
    rms = audioop.rms(data, 2)
    decibel = 20 * math.log10(rms)
    decibel = str(decibel)
    now = datetime.now()
    ts = now.strftime("%H:%M:%S")
    ts = str(ts)
    temp_array = np.array([ts, decibel])
    merged_array = np.vstack((decibel_array, temp_array))

    return merged_array


def serial_recording(file_name, serial_port):
    serial_file = file_name + ".csv"
    getdata = serial_port.readline()
    data = getdata.decode('utf-8')
    print(data)
    file = open(serial_file, "a")
    file.write(data + "\n")
    file.close()


def main():
    start_spikerbox()
    time.sleep(10)
    stop_spikerbox()
    '''global sample_number

    while True:
        try:
            sample_number = int(input("Sample number to collect: "))
            break
        except ValueError:
            print("Please input integer only...")
            continue
    decibel_array = np.array(["Time", "Decibel"])
    arduino_port = "COM5"
    baud = 9600
    file_name = input("File name: ")
    line = 0
    serial_port = serial.Serial(arduino_port, baud)
    while line <= sample_number:
        serial_recording(file_name, serial_port)
        decibel_array = decibel_recording(decibel_array)
        line = line + 1

    pd.DataFrame(decibel_array).to_csv(file_name + "_decibel.csv", index=False)
    print("Data collection complete!")
    '''

if __name__ == '__main__':
    main()
