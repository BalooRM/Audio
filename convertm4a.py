#!/usr/bin/python
from pydub import AudioSegment
import sys
import re

appname = "convertwav.py"
gaindB = 30

usage = """  This script reads an input M4A file and converts it to
  MP3 with a """ + str(gaindB) + """ dB gain.  

Usage: 
 > python """ + appname + """ FILENAME.WAV

Output: FILENAME_converted.mp3
"""

myargs = sys.argv    # read command line args
if len(myargs) < 2:  # if there are not enough args, print usage and exit
    print("ERROR: not enough parameters.\n")
    sys.exit(usage)
infile = myargs[1]
if not re.search("\.m4a$", infile, re.IGNORECASE):
    print("ERROR: Input", infile, "is not an M4A file.\n")
    sys.exit(usage)

outfile = infile.split('.')[0] + "_converted.mp3"

print("Input =", infile)
print("Output =", outfile)

# files                                                                         
src = infile
dst = outfile
print("Preparing to convert M4A file to MP3")
input("Press Enter to continue...")
#sys.exit("Goodbye")
print("Converting from M4A to MP3...")

# convert m4a to mp3                                                            
sound = AudioSegment.from_file(src, format="m4a")
sound = sound + gaindB
sound.export(dst, format="mp3")
