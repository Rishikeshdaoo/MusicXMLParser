# import xml.etree.ElementTree as et
from music21 import *


song = converter.parse('E:/SensiBol/MusicXML/Vaccai_1.musicxml')

for a in song.recurse.notes:
