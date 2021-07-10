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
import pydirectinput
import os

spike_recorder_path = "C:\Program Files (x86)/Backyard Brains/Spike Recorder/SpikeRecorder.exe"
arduino_port = "COM3"
audio_file = "construction.mp3"
baud = 9600
SAMPLING_RATE = 22050
NUM_SAMPLES = 2048
connect_button_x = 200
connect_button_y = 58
record_button_x = 1193
record_button_y = 58
cancle_record_button_x = 2655
cancle_record_button_y = 177

print(connect_button_x)


def start_spikerbox():
    subprocess.Popen(spike_recorder_path)
    time.sleep(2)
    pyautogui.hotkey('winleft', 'up')
    time.sleep(5)

    pydirectinput.click(connect_button_x, connect_button_y, duration=0.25)
    pydirectinput.click(record_button_x, record_button_y, duration=0.25)


def stop_spikerbox():
    pydirectinput.click(cancle_record_button_x, cancle_record_button_y)


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
    try:
        file = open(serial_file, "a")

    except PermissionError:
        print("Cannot read csv, trying again...")

    file.write(data + "\n")
    file.close()


def main():
    global record_time

    while True:
        try:
            record_time = int(input("Add a record time in minutes (integers only): "))
            break
        except ValueError:
            print("Please input integer only...")
            continue

    decibel_array = np.array(["Time", "Decibel"])

    file_name = input("File name: ")
    attempt_counter = 0
    attempt_max = 5

    while attempt_counter < attempt_max:
        try:
            serial_port = serial.Serial(arduino_port, baud)
            break
        except serial.SerialException:
            print('Serial port occupied, trying again...')
            attempt_counter += 1
            if attempt_counter == attempt_max:
                print('Terminating')
                exit()
            continue
    # start_spikerbox()
    record_time = record_time * 60
    time_end = time.time() + record_time
    os.system('start ' + audio_file)
    while time.time() < time_end:
        serial_recording(file_name, serial_port)
        decibel_array = decibel_recording(decibel_array)
        print(decibel_array)

    pd.DataFrame(decibel_array).to_csv(file_name + "_decibel.csv", index=False)
    stop_spikerbox()
    print("Data collection complete!")


if __name__ == '__main__':
    main()
