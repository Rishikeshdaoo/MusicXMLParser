import struct
import xml.etree.ElementTree as et
import math
import wave
import numpy as np
from scipy.io.wavfile import read
from scipy.io.wavfile import write

tempo = 0.0
beats = []
beat_size = []
iter = 0
sampling_rate = 44100.0
audio = []
upbeat = []
downbeat = []
silence = []

tree = et.parse('E:/MusicXML/Down_In_The_River_To_Pray_New.musicxml')
root = tree.getroot()

for sound in root.iter('sound'):
    if 'tempo' in sound.attrib.keys():
        tempo = int(float(sound.attrib.get('tempo')))

temp_beat = 0
temp_size = 0
for measures in root.iter('measure'):
    for measureChild in measures:
        if measureChild.tag == 'attributes':
            for attribChild in measureChild:
                if attribChild.tag == 'time':
                    for timeChild in attribChild:
                        if timeChild.tag == 'beats':
                            temp_beat = int(timeChild.text)
                        if timeChild.tag == 'beat-type':
                            temp_size = int(timeChild.text)

    beats.append(temp_beat)
    beat_size.append(temp_size)
    iter += 1

iter = int(iter/2)
beats = beats[:iter]
beat_size = beat_size[:iter]

print(iter, beats, beat_size)

# import sys
# sys.exit()


def click(duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    global audio
    global upbeat
    global downbeat

    num_samples = int(float(duration_milliseconds * (sampling_rate / 1000.0)))
    samples_per_beat = int(float((60.0 / tempo) * sampling_rate))
    # iterations = int(num_samples / (samples_per_beat* beats))

    for silenceSamp in range(samples_per_beat - 5000):
        silence.append(0.0)

    _, upbeat_wav = read('E:/MusicXML/metronomeup.wav')
    _, downbeat_wav = read('E:/MusicXML/metronomedown.wav')

    upbeat = upbeat_wav[:, 1]
    downbeat = downbeat_wav[:, 1]

    upbeat = upbeat / upbeat.max()
    downbeat = downbeat / downbeat.max()

    upbeat = upbeat[0:5000]
    downbeat = downbeat[0:5000]

    for n in range(iter):
        for current_beat in range(beats[n]):
            if current_beat == 0:
                audio.extend(upbeat)
            else:
                audio.extend(downbeat)

            audio.extend(silence)

    return


def save_wav(file_name):
    # Open up a wav file
    wav_file = wave.open(file_name, "w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sampling_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))

    wav_file.close()

    return


click(8000)
save_wav("E:/metroTest.wav")
