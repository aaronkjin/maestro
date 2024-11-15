from typing import List
from midiutil import MIDIFile

def save_melody_as_midi(melody: List[str], filename: str):
    """Save a melody as a MIDI file."""
    midi = MIDIFile(1)  # One track
    track = 0
    time = 0
    tempo = 120
    
    midi.addTempo(track, time, tempo)
    
    for i, note in enumerate(melody):
        if note != 'START':
            # Convert note to MIDI pitch
            note_name = note[0]
            octave = int(note[-1])
            base_notes = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
            pitch = base_notes[note_name] + (octave - 4) * 12
            
            # Add note to MIDI file
            midi.addNote(track, 0, pitch, time + i, 1, 100)
    
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)