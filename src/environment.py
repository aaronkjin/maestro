from typing import List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum

class Duration(Enum):
    SIXTEENTH = 0.25  # 1/4 beat
    EIGHTH = 0.5      # 1/2 beat
    QUARTER = 1.0     # 1 beat
    HALF = 2.0        # 2 beats
    WHOLE = 4.0       # 4 beats

@dataclass
class Note:
    pitch: str
    duration: Duration
    
    def __str__(self):
        return f"{self.pitch}_{self.duration.name}"

class MusicEnvironment:
    def __init__(self):
        # Notes in C major scale: C4 to C5
        self.notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
        self.durations = list(Duration)
        
        self.n_actions = len(self.notes) * len(self.durations)
        
        self.action_to_note = {}
        self.note_to_action = {}
        idx = 0
        for note in self.notes:
            for duration in self.durations:
                note_obj = Note(note, duration)
                self.action_to_note[idx] = note_obj
                self.note_to_action[str(note_obj)] = idx
                idx += 1
        
        self.beats_per_measure = 4
        self.measures_per_phrase = 4    
        self.num_phrases = 8     
        self.total_beats = self.beats_per_measure * self.measures_per_phrase * self.num_phrases
        
        self.current_beat = 0.0
        self.current_measure = 0
        self.current_phrase = 0
        self.state = [Note('START', Duration.QUARTER)] * 3
        self.measure_notes = []
        self.phrase_notes = []
        
        # Common rhythm patterns
        self.rhythm_patterns = {
            'basic': [Duration.QUARTER] * 4,
            'waltz': [Duration.QUARTER, Duration.EIGHTH, Duration.EIGHTH],
            'syncopated': [Duration.EIGHTH, Duration.QUARTER, Duration.EIGHTH],
            'long_short': [Duration.HALF, Duration.QUARTER, Duration.QUARTER]
        }
    

    def _is_valid_duration(self, duration: Duration) -> bool:
        return self.current_beat % self.beats_per_measure + duration.value <= self.beats_per_measure
    

    def _is_measure_complete(self) -> bool:
        return self.current_beat % self.beats_per_measure == 0 and self.current_beat > 0
    

    def _is_phrase_complete(self) -> bool:
        return self.current_measure % self.measures_per_phrase == 0 and self.current_measure > 0
    

    def _calculate_rhythm_reward(self, note: Note) -> float:
        reward = 0
        
        # Reward for proper measure timing
        if self._is_valid_duration(note.duration):
            reward += 1
        else:
            reward -= 5
            
        # Reward for rhythmic variety within measure
        if self.measure_notes:
            last_duration = self.measure_notes[-1].duration

            if note.duration != last_duration:
                reward += 0.5
                
        # Reward for common rhythmic patterns
        measure_durations = [n.duration for n in self.measure_notes] + [note.duration]

        for pattern in self.rhythm_patterns.values():
            if len(measure_durations) >= len(pattern):
                if measure_durations[-len(pattern):] == pattern:
                    reward += 2 
        
        # Reward for proper phrase endings
        if self._is_phrase_complete():
            if note.duration in [Duration.HALF, Duration.WHOLE]:
                reward += 2  
        
        return reward
    

    def _calculate_melodic_reward(self, note: Note) -> float:
        reward = 0
        
        current_midi = self._note_to_midi(note.pitch)
        
        if self.state[-1].pitch != 'START':
            prev_midi = self._note_to_midi(self.state[-1].pitch)
            
            interval = abs(current_midi - prev_midi)
            if interval <= 2 and note.duration in [Duration.EIGHTH, Duration.SIXTEENTH]:
                reward += 1
            
            if interval >= 4 and note.duration in [Duration.HALF, Duration.WHOLE]:
                reward += 1
        
        if len(self.phrase_notes) >= 2:
            if note.pitch == self.phrase_notes[-1].pitch == self.phrase_notes[-2].pitch:
                reward -= 8
                
        return reward
    

    def _calculate_reward(self, note: Note) -> float:
        rhythm_reward = self._calculate_rhythm_reward(note)
        melodic_reward = self._calculate_melodic_reward(note)
        
        reward = rhythm_reward + melodic_reward
        
        if self.current_beat >= self.total_beats - self.beats_per_measure:
            if note.pitch == 'C4' and note.duration == Duration.WHOLE:
                reward += 5
        
        return reward
    

    def _note_to_midi(self, note: str) -> int:
        if note == 'START':
            return 0
        
        base_notes = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
        note_name = note[0]
        octave = int(note[-1])

        return base_notes[note_name] + (octave - 4) * 12
    
    
    def reset(self) -> str:
        self.current_beat = 0.0
        self.current_measure = 0
        self.current_phrase = 0
        self.state = [Note('START', Duration.QUARTER)] * 3
        self.measure_notes = []
        self.phrase_notes = []

        return str(self.state)
    

    def step(self, action: int) -> Tuple[str, float, bool, Dict]:
        note = self.action_to_note[action]
        
        reward = self._calculate_reward(note)
        
        self.current_beat += note.duration.value
        if self._is_measure_complete():
            self.current_measure += 1
            self.measure_notes = []
        if self._is_phrase_complete():
            self.current_phrase += 1
            self.phrase_notes = []

        self.state = self.state[1:] + [note]
        self.measure_notes.append(note)
        self.phrase_notes.append(note)
        
        done = self.current_beat >= self.total_beats
        
        return str(self.state), reward, done, {
            'current_beat': self.current_beat,
            'current_measure': self.current_measure,
            'measure_complete': self._is_measure_complete()
        }