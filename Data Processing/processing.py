from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy

#samplerate, data = wavfile.read("./Data/Big-Mimosa/bm_no_sound.wav")
#plant = "Mini-Mimosa"
#plant = "Big-Mimosa"
#plant = "Basil"p
plant = "Chili"
samplerate, data = wavfile.read("./Data/"+plant+"/no_sound.wav")
sampleratet1, datat1 = wavfile.read("./Data/"+plant+"/traffic1.wav")
sampleratet2, datat2 = wavfile.read("./Data/"+plant+"/traffic2.wav")
sampleratet3, datat3 = wavfile.read("./Data/"+plant+"/traffic3.wav")
sampleratec1, datac1 = wavfile.read("./Data/"+plant+"/con1.wav")
sampleratec2, datac2 = wavfile.read("./Data/"+plant+"/con2.wav")
sampleratec3, datac3 = wavfile.read("./Data/"+plant+"/con3.wav")
#samplerate, data = wavfile.read("./Data/Big-Mimosa/bm_no_sound.wav")
#samplerate, data = wavfile.read("./Data/Big-Mimosa/bm_no_sound.wav")

def myprint(sample, data, txt):
    print(sample)
    print(data)
    plt.figure(txt)
    plt.title(txt)
    plt.plot(data)
    #plot selected data points
    #plt.plot(data[0:1800000])
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    #maximalwert
    print('Maximum:', numpy.amax(data))
    #minimalwert
    print('Minimum:', numpy.amin(data))
    #differenz zwischen minimum und maximum
    print('Amplitude:', numpy.ptp(data))
    #median
    print('Median:', numpy.median(data))
    #durchschnittlicher wert
    print('Durchschnitt:', numpy.mean(data))
    #print(numpy.average(data))
    #limit x
    #plt.xlim(0, 10000)
    plt.show()

myprint(samplerate, data, plant+"_no_sound")
myprint(sampleratet1, datat1, plant+"_traffic1")
myprint(sampleratet2, datat2, plant+"_traffic2")
myprint(sampleratet3, datat3, plant+"_traffic3")
myprint(sampleratec1, datac1, plant+"_con1")
myprint(sampleratec2, datac2, plant+"_con2")
myprint(sampleratec3, datac3, plant+"_con3")

    

