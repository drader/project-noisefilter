from scipy.fft import rfft, irfft, rfftfreq
from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = [16, 12]
plt.rcParams.update({'font.size': 18})

###################### Take input file and create variables
fs, data = wavfile.read('./sound1.wav')
f = (data / 2.0**31)
nyq = fs/2
dt = 1/fs
n = f.shape[0]
duration = n/fs
time = np.arange(0,duration,dt)

plt.plot(time, f, 'b')
plt.show()
####################### FFT Computation
signal = f[:,0]
data_fft = rfft(signal)
freq = rfftfreq(signal.size, d=1./fs)
L = np.arange(1,np.floor(n/2),dtype='int')
data_fft_abs = np.abs(data_fft)

plt.plot(freq, data_fft_abs)
plt.xlabel("frequency, Hz")
plt.ylabel("Amplitude, units")
plt.show()

# Looking at amplitudes of the spikes higher than 200
"""for i,f in enumerate(data_fft_abs):
    if f>200:  
        print('frequency = {} Hz with amplitude {} '.format(np.round(freq[i],1),  np.round(f)))"""

# Noise Filter for 250Hz and 400Hz
for i,f in enumerate(freq):
    if (f < 251 and f > 249):
        data_fft[i] = 0.0
    if (f < 401 and f > 399):
        data_fft[i] = 0.0

output = irfft(data_fft)



####################### Plots
fig,axs = plt.subplots(3,1)
plt.sca(axs[0])
plt.plot(time, signal, 'c', LineWidth = 1.5, label = 'Noisy')
plt.xlim(time[0],time[-1])
plt.legend()

plt.sca(axs[1])
plt.plot(time, output, 'b', LineWidth = 2, label = 'Filtered')
plt.xlim(time[0],time[-1])
plt.legend()

plt.sca(axs[2])
plt.plot(freq[L],data_fft_abs[L], 'c', LineWidth = 2, label = 'Noisy')
plt.plot(freq[L],output[L],'r', LineWidth = 1.5, label = 'Filtered')
plt.xlim(freq[L[0]],freq[L[-1]])
plt.legend() 

plt.show()

wavfile.write("output.wav", fs, output)