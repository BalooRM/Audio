#!/usr/bin/python
from pydub import AudioSegment
import sys
import re

appname = "convertwav.py"
gaindB = 30
silencethold = -60.0
leadingtime = 1000  # milliseconds

usage = """  This script reads an input WAV file and converts it to
  MP3 with a """ + str(gaindB) + """ dB gain.  

Usage: 
 > python """ + appname + """ FILENAME.WAV

Output: FILENAME_converted.mp3
"""

def detect_leading_silence(sound, silence_threshold=silencethold, chunk_size=100):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size
        #print("trim_ms\t" + str(trim_ms) + "\tdBFS\t" + str(sound[trim_ms:trim_ms+chunk_size].dBFS))

    return trim_ms


myargs = sys.argv    # read command line args
if len(myargs) < 2:  # if there are not enough args, print usage and exit
    print("ERROR: not enough parameters.\n")
    sys.exit(usage)
infile = myargs[1]
if not re.search("\.WAV$", infile, re.IGNORECASE):
    print("ERROR: Input", infile, "is not a WAV file.\n")
    sys.exit(usage)

outfile = infile.split('.')[0] + "_converted.mp3"

print("Input =", infile)
print("Output =", outfile)

# files                                                                         
src = infile
dst = outfile
print("Preparing to convert WAV file to MP3 with a " + str(gaindB) + " dB gain.")
print("A " + str(silencethold) + " dB silence threshhold will be applied to the start.")
print("Conversion will begin up to " + str(leadingtime) + " milliseconds before silence threshhold detection.")
input("Press Enter to continue...")
#sys.exit("Goodbye")
print("Converting from WAV to MP3...")

# convert wav to mp3                                                            
sound = AudioSegment.from_wav(src)
duration = len(sound)
print("Track duration = " + str(len(sound)) + " milliseconds.")

trim_start = detect_leading_silence(sound)
print("trim_start = " + str(trim_start))
trim_start = max([0,trim_start - leadingtime])
print("trim_start = " + str(trim_start))

#trim_end = detect_leading_silence(sound.reverse())   # trim silence from the end
trim_end = 0
print("trim_end = " + str(trim_end))

extractduration = duration - trim_end - trim_start
print("Extracting " + str(extractduration) + " milliseconds.")
sound = sound[trim_start:duration-trim_end]
print(str(trim_start/1000.0) + " seconds trimmed from start.")
print(str(trim_end/1000.0) + " seconds trimmed from end.")
# apply gain factor
chan = sound.split_to_mono()     # split multiple channels into mono
sound = sound + gaindB
sound.export(dst, format="mp3")

for i in range(0, sound.channels):
    print("Channel " + str(i))
    if (trim_start > 0):
        print("Average background level = ", str(chan[i][0:trim_start].dBFS))
    dst = infile.split('.')[0] + "_chan" + str(i) + ".mp3"
    print("Writing channel output to " + dst)
    chan[i] = chan[i] + gaindB
    chan[i].export(dst, format="mp3")

print("Conversion complete.")
input("Press Enter to continue...")
