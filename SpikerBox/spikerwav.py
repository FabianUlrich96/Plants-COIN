from scipy.io import wavfile
import matplotlib.pyplot as plt

samplerate, data = wavfile.read('wav_test.wav')

print(samplerate)
print(data)

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(data)
plt.show()