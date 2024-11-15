from typing import List, Tuple, Dict

class MusicEnvironment:
    def __init__(self):
        # Define notes in C major scale (C4 to C5)
        self.notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
        self.note_to_idx = {note: idx for idx, note in enumerate(self.notes)}
        self.idx_to_note = {idx: note for idx, note in enumerate(self.notes)}
        
        # State will be last two notes played (to check for repetition)
        self.state = ['START', 'START']  # Special start state
        self.max_steps = 32  # Length of melody to generate
        self.current_step = 0
        
        # Define consonant intervals (in semitones)
        self.consonant_intervals = [0, 3, 4, 5, 7, 8, 9]
        
        # Keep track of note counts to prevent excessive repetition
        self.note_counts = {note: 0 for note in self.notes}
    
    def reset(self) -> str:
        """Reset the environment to initial state."""
        self.state = ['START', 'START']
        self.current_step = 0
        self.note_counts = {note: 0 for note in self.notes}
        return str(self.state)
    
    def _calculate_reward(self, note: str) -> float:
        """Calculate reward based on music theory rules."""
        reward = 0
        
        if note == self.state[-1] and note == self.state[-2]:
            reward -= 5
        
        if self.state[-1] != 'START':
            last_note = self.state[-1]
            current_midi = self._note_to_midi(note)
            last_midi = self._note_to_midi(last_note)
            interval = abs(current_midi - last_midi)
            
            if interval in self.consonant_intervals:
                reward += 2
            else:
                reward -= 2
                
        if self.note_counts[note] > 3:
            reward -= 2
            
        return reward
    
    def _note_to_midi(self, note: str) -> int:
        """Convert note name to MIDI number."""
        if note == 'START':
            return 0
        
        base_notes = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
        note_name = note[0]
        octave = int(note[-1])
        return base_notes[note_name] + (octave - 4) * 12
    
    def step(self, action: int) -> Tuple[str, float, bool, Dict]:
        """Take a step in the environment."""
        note = self.idx_to_note[action]
        self.note_counts[note] += 1
        reward = self._calculate_reward(note)
        self.state = [self.state[-1], note]
        self.current_step += 1
        done = self.current_step >= self.max_steps
        return str(self.state), reward, done, {}