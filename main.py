from src.environment import MusicEnvironment
from src.agent import QLearningAgent
from src.train import train_agent, generate_melody
from src.utils import (
    save_melody_as_midi, 
    format_melody_for_display, 
    analyze_melody, 
    print_melody_analysis,
    visualize_rhythm_pattern
)
import matplotlib.pyplot as plt


def plot_rewards(rewards):
    plt.figure(figsize=(10, 5))
    plt.plot(rewards)
    plt.title('Training Rewards over Episodes')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.savefig('outputs/training_rewards.png')
    plt.close()


def main():
    env = MusicEnvironment()
    agent = QLearningAgent(n_actions=env.n_actions)
    
    print("Training agent...")
    rewards = train_agent(env, agent, n_episodes=100)
    plot_rewards(rewards)
    
    print("\nGenerating melody...")
    melody = generate_melody(env, agent)
    
    print("\nComplete Melody:")
    print(format_melody_for_display(melody))
    
    print("\nRhythm pattern by phrase:")
    for i in range(env.num_phrases):
        start_idx = i * (env.measures_per_phrase * env.beats_per_measure)
        end_idx = start_idx + (env.measures_per_phrase * env.beats_per_measure)
        phrase_melody = melody[start_idx:end_idx]
        print(f"\nPhrase {i+1}:")
        print(visualize_rhythm_pattern(phrase_melody))
    
    midi_filename = "outputs/melodies/melody.mid"
    save_melody_as_midi(melody, midi_filename, tempo=100)
    print(f"\nSaved as {midi_filename}")
    
    analysis = analyze_melody(melody)
    print_melody_analysis(analysis)
    
    print("\nPhrase Analysis:")
    for i in range(env.num_phrases):
        start_idx = i * (env.measures_per_phrase * env.beats_per_measure)
        end_idx = start_idx + (env.measures_per_phrase * env.beats_per_measure)
        phrase_melody = melody[start_idx:end_idx]
        phrase_analysis = analyze_melody(phrase_melody)
        print(f"\nPhrase {i+1}:")
        print(f"- Total beats: {phrase_analysis['total_beats']}")
        print(f"- Number of notes: {phrase_analysis['note_count']}")
        print(f"- Average interval: {phrase_analysis['avg_interval']:.2f} semitones")

if __name__ == "__main__":
    main()