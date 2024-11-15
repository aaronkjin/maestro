import pygame
import time
import sys
from pathlib import Path


def play_midi(midi_file):
    try:
        # Pygame mixer for loading and playing sounds
        pygame.mixer.init()
        pygame.mixer.music.load(midi_file)
        
        print(f"Playing {midi_file}...")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(1)
            
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        print("\nPlayback stopped by user")

    except Exception as e:
        print(f"Error playing MIDI file: {e}")

    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    # Play all melodies
    melody_dir = Path("outputs/melodies")
    midi_files = list(melody_dir.glob("*.mid"))
    
    if not midi_files:
        print("No MIDI files found in outputs/melodies/")
        sys.exit(1)
    
    print(f"Found {len(midi_files)} MIDI files")

    for midi_file in midi_files:
        play_midi(midi_file)
        time.sleep(1)