from midiutil import MIDIFile
from mido import MidiTrack
from typing import List
from .environment import Note, Duration
import random

drum_to_midi = {
    "kick": 36,
    "snare": 38,  
    "hihat_closed": 42, 
    "hihat_open": 46    
}

drum_patt = {
    "sync": [
        ("kick", 0), ("hihat_closed", 0.5),
        ("kick", 1), ("hihat_open", 1.25), ("snare", 1.75),
        ("kick", 2), ("hihat_closed", 2.5), ("snare", 3.25)
    ]
}


def duration_to_beats(duration: Duration) -> float:
    return duration.value


def add_crescendo_decrescendo(
    midi: MIDIFile, 
    track: int, 
    pitch: int, 
    start_time: float, 
    duration: float, 
    start_velocity: int, 
    end_velocity: int
):
    num_steps = 8 
    step_duration = duration / num_steps  
    velocity_step = (end_velocity - start_velocity) / num_steps  

    current_time = start_time
    current_velocity = start_velocity

    for i in range(num_steps):
        midi.addNote(track, 0, pitch, current_time, step_duration, int(current_velocity))
        current_time += step_duration
        current_velocity += velocity_step


def save_melody_as_midi(melody: List[Note], filename: str, tempo: int = 120):
    midi = MIDIFile(2)
    track = 0
    time = 0
    
    midi.addTempo(track, time, tempo)
    
    
    max_time = 0
    for note in melody:
        if note.pitch != 'START':
            note_name = note.pitch[0]
            octave = int(note.pitch[-1])
            base_notes = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
            pitch = base_notes[note_name] + (octave - 4) * 12
            
            duration = duration_to_beats(note.duration)
            if duration >= 4:
                if random.random() < 0.3:
                    add_crescendo_decrescendo(midi, 0, pitch, time, duration, 60, 90)
                    add_crescendo_decrescendo(midi, 0, pitch + 4, time, duration, 60, 90)
                    add_crescendo_decrescendo(midi, 0, pitch + 7, time, duration, 60, 90)
                else:
                    add_crescendo_decrescendo(midi, 0, pitch, time, duration, 90, 30)
                    add_crescendo_decrescendo(midi, 0, pitch + 4, time, duration, 90, 30)
                    add_crescendo_decrescendo(midi, 0, pitch + 7, time, duration, 90, 30)
            else:
                vel = 50 if duration <= 1 else 100
                midi.addNote(track, 0, pitch, time, duration, vel)
                time += duration
            max_time = time
    
    drum_pattern = drum_patt['sync']
    t = max_time
    for beat in range((int)(t)):
        for drum, offset in drum_pattern:
            drum_note = drum_to_midi[drum]
            note_time = beat + offset
            midi.addNote(1, 9, drum_note, note_time, 0.25, 25)
    
    
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)


def format_melody_for_display(melody: List[Note]) -> str:
    formatted = []
    current_measure = []
    current_beats = 0
    
    for note in melody:
        if note.pitch != 'START':
            note_str = f"{note.pitch}({note.duration.name})"
            current_measure.append(note_str)
            current_beats += note.duration.value
            
            if current_beats >= 4:
                formatted.append(" ".join(current_measure))
                current_measure = []
                current_beats = 0
    
    if current_measure:
        formatted.append(" ".join(current_measure))
    
    return "\n".join(formatted)


def analyze_melody(melody: List[Note]) -> dict:
    analysis = {
        'total_beats': 0,
        'note_count': 0,
        'duration_distribution': {d: 0 for d in Duration},
        'pitch_distribution': {},
        'avg_interval': 0,
        'intervals': []
    }
    
    prev_midi = None
    
    for note in melody:
        if note.pitch != 'START':
            analysis['duration_distribution'][note.duration] += 1
            analysis['total_beats'] += note.duration.value
            analysis['note_count'] += 1
            
            if note.pitch not in analysis['pitch_distribution']:
                analysis['pitch_distribution'][note.pitch] = 0
            analysis['pitch_distribution'][note.pitch] += 1
            
            note_name = note.pitch[0]
            octave = int(note.pitch[-1])
            base_notes = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
            current_midi = base_notes[note_name] + (octave - 4) * 12
            
            if prev_midi is not None:
                interval = abs(current_midi - prev_midi)
                analysis['intervals'].append(interval)
            
            prev_midi = current_midi
    
    if analysis['intervals']:
        analysis['avg_interval'] = sum(analysis['intervals']) / len(analysis['intervals'])
    
    return analysis


def print_melody_analysis(analysis: dict):
    print("\nMelody Analysis:")
    print(f"Total beats: {analysis['total_beats']}")
    print(f"Number of notes: {analysis['note_count']}")
    
    print("\nDuration Distribution:")
    for duration, count in analysis['duration_distribution'].items():
        if count > 0:
            print(f"{duration.name}: {count} notes ({count/analysis['note_count']*100:.1f}%)")
    
    print("\nPitch Distribution:")
    for pitch, count in sorted(analysis['pitch_distribution'].items()):
        print(f"{pitch}: {count} times ({count/analysis['note_count']*100:.1f}%)")
    
    print(f"\nAverage interval size: {analysis['avg_interval']:.2f} semitones")


def visualize_rhythm_pattern(melody: List[Note], measures_per_line: int = 4):
    symbols = {
        Duration.WHOLE: 'w',
        Duration.HALF: 'h',
        Duration.QUARTER: 'q',
        Duration.EIGHTH: 'e',
        Duration.SIXTEENTH: 's'
    }
    
    visualization = []
    current_line = []
    current_beats = 0
    measure_count = 0
    
    for note in melody:
        if note.pitch != 'START':
            if current_beats == 0:
                current_line.append('|')
            
            current_line.append(symbols[note.duration])
            current_beats += note.duration.value
            
            if current_beats >= 4:
                measure_count += 1
                current_beats = 0
                
                if measure_count % measures_per_line == 0:
                    current_line.append('|')
                    visualization.append(' '.join(current_line))
                    current_line = []
    
    if current_line:
        if current_line[-1] != '|':
            current_line.append('|')
        visualization.append(' '.join(current_line))
    
    return '\n'.join(visualization)