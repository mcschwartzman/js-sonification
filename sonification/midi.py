import pandas as pd

from midiutil import MIDIFile
from random import randrange

degrees = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
track = 0
channel = 0
time = 0    # In beats
duration = 1    # In beats
tempo = 180   # In BPM
volume = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
# automatically)
MyMIDI.addTempo(track, time, tempo)

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
octaves = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
durations = [1, 2, 3, 4]

for i, pitch in enumerate(degrees):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)


def getMIDNum(note, octave):

    placement = octave + 2

    index = notes.index(note)

    result = index + (placement * 12)

    if result < 0:

        result = 0

    elif result > 127:

        result = 127

    return result


def subprocess(item, slice):

    # take a slice tuple to find an integer and return the new int

    new = str(item)[slice[0]:slice[1]]

    return new


def noise(length):

    path = [randrange(127) for i in range(0, length)]

    return path


def normalize(array):

    array.sort()

    unique = set(array)

    return unique


def values(file, octave_key=None, note_key=None, duration_key=None):

    df = pd.read_csv(file)

    octave_scale = scale(octave_key, 'aisle', df=df)
    octave_mult = len(octave_scale) / 11  # number of octaves

    note_scale = scale(note_key, 'location', df=df)
    note_mult = len(note_scale) / 12  # number of notes

    duration_scale = scale(duration_key, 'quantity', df=df)
    duration_mult = len(duration_scale) / 4

    print(duration_scale)

    return [{
        'octave': int(octave_scale.index(df['aisle'][i]) / octave_mult),
        'note':int(note_scale.index(df['location'][i]) / note_mult),
        'duration':int(duration_scale.index(df['quantity'][i]) / duration_mult)
    } for i in range(df.shape[0])]


def scale(scale, header, df):

    if(scale):  # key scale provided from known values

        return scale

    else:  # derive key scale from data values

        scale = [key for key in df[header]]
        return [key
                for key in normalize(scale)]


aisles = [
    "right_aisle",
    "a12",
    "left_aisle",
    "a29",
    "a28",
    "a27",
    "a26",
    "a25",
    "a24",
    "a23",
    "a22",
    "a21",
    "a20",
    "a19",
    "a18",
    "a17",
    "a16",
    "a15",
    "a14",
    "a13",
    "37_left",
    "a06",
    "a07",
    "a08",
    "a10",
    "a11"
]

DataMIDI = MIDIFile(1)
DataMIDI.addTempo(track, time, tempo)


def sequential(file):   # does not use timestamps, recommended to assume even timing

    for i, obj in enumerate(values(file=file, octave_key=aisles, duration_key=list(range(300)))):

        pitch = getMIDNum(note=notes[obj['note']],
                          octave=octaves[obj['octave']])

        DataMIDI.addNote(track, channel, pitch, time + i,
                         durations[obj['duration']], volume)

sequential(file='soup.csv')

with open("output.mid", "wb") as writeFile:
    DataMIDI.writeFile(writeFile)
