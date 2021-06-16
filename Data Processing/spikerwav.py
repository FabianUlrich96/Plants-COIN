from scipy.io import wavfile
import matplotlib.pyplot as plt

samplerate, data = wavfile.read('BYB_Recording_2021-06-13_14.59.03.wav')

print(samplerate)
print(data)

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(data)
plt.show()