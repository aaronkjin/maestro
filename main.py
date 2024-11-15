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
import os

def plot_rewards(rewards):
    plt.figure(figsize=(10, 5))
    plt.plot(rewards)
    plt.title('Training Rewards over Episodes')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.savefig('outputs/training_rewards.png')
    plt.close()

def main():
    # Create environment and agent
    env = MusicEnvironment()
    agent = QLearningAgent(n_actions=env.n_actions)
    
    # Train the agent
    print("Training agent...")
    rewards = train_agent(env, agent, n_episodes=20000)
    plot_rewards(rewards)
    
    # Generate multiple melodies
    print("\nGenerating melodies...")
    for i in range(5):
        melody = generate_melody(env, agent)
        
        print(f"\nMelody {i+1}:")
        print(format_melody_for_display(melody))
        
        print("\nRhythm pattern:")
        print(visualize_rhythm_pattern(melody))
        
        # Save as MIDI
        midi_filename = f"outputs/melodies/rhythmic_melody_{i+1}.mid"
        save_melody_as_midi(melody, midi_filename)
        print(f"Saved as {midi_filename}")
        
        # Analyze the melody
        analysis = analyze_melody(melody)
        print_melody_analysis(analysis)
        print("\n" + "="*50)

if __name__ == "__main__":
    main()