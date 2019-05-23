"""
Name:           Carlos Meza
Description:
 
"""


import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# Gets both fft results and returns the highest value for plotting
def get_max(temp1, temp2):
    value1 = max(temp1)
    value2 = max(temp2)
    
    if(value1 > value2):
        return value1 + 100
    else:
        return value2 + 100


def applyShelvingFilter(inName, outName, g, fc) :
    # Read soundfile and get its length
    data, samplerate = sf.read(inName)
    length = int(len(data))
    # Get constants, arange with samplerate and get length of plot
    fs = samplerate / length
    x = np.arange(0, samplerate//4, fs)
    # Create an array to populate and normalized cutoff freq and u
    u = np.ones(length)
    y = np.ones(length)
    # Get theta, mu, gamma and alpha
    Oc = (2*np.pi*fc) / fs
    mu = 10**(g / 20)
    gamma = (1-(4/(1+mu))*np.tan(Oc/2))/(1+(4/(1+mu))*np.tan(Oc/2))
    alpha = (1 - gamma) / 2
    
    # Loop and populate with added gain and boost
    for i in range(length):
        # Initialize first value of array to 0 since theres no i < 0
        if(i < 1):
            u[i] = alpha * (data[i] + 0) + gamma * 0
            y[i] = u[i] * (mu - 1) + data[i]
        # Get previous values of data and apply it to equation below
        else:
            u[i] = alpha * (data[i] + data[i - 1]) + gamma * u[i - 1]
            y[i] = u[i] * (mu - 1) + data[i]
    
    # Get fft from original wav file
    fft = np.fft.fft(data)
    fft.resize(length//4)
    # Get fft of the edited wave file
    fft_y = np.fft.fft(y)
    # Get clean file to write out before resizing
    clean = np.fft.ifft(fft_y)
    fft_y.resize(length//4)
    
    # Use get max function to return highest value from both fft results
    max_value = get_max(abs(fft), abs(fft_y))
    
    # Plot Original data w/ fft
    plt.subplot(1,2,1)
    plt.ylim(0, max_value)
    plt.title('Original Signal')
    plt.plot(x, abs(fft))
    
    # Plot Original data w/ fft
    plt.subplot(1,2,2)
    plt.ylim(0, max_value)
    plt.title('Filtered Signal')
    plt.plot(x, abs(fft_y))
    plt.show()
    
    # Get only the real values of wav file
    clean = np.real(clean)
    # Write out to wav file the clean version(inverse fft) of sound file
    sf.write(outName, clean, samplerate)


##########################  main  ##########################
if __name__ == "__main__" :
    inName = "P_9_1.wav"
    gain = -10  # can be positive or negative
                # WARNING: small positive values can greatly amplify the sounds
    cutoff = 300
    outName = "shelvingOutput.wav"

    applyShelvingFilter(inName, outName, gain, cutoff)