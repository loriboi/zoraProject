from scipy.io import wavfile
import noisereduce as nr

def reduceNoise(file):
    rate, data = wavfile.read(file)

    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    reduce_file = file+'_red.wav'
    wavfile.write(reduce_file, rate, reduced_noise)
    return reduce_file