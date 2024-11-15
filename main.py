from src.environment import MusicEnvironment
from src.agent import QLearningAgent
from src.train import train_agent, generate_melody
from src.utils import save_melody_as_midi
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
    # Create environment and agent
    env = MusicEnvironment()
    agent = QLearningAgent(n_actions=len(env.notes))
    
    # Train the agent
    print("Training agent...")
    rewards = train_agent(env, agent, n_episodes=1000)
    plot_rewards(rewards)
    
    # Generate and save multiple melodies
    print("\nGenerating melodies...")
    for i in range(5):
        melody = generate_melody(env, agent)
        print(f"\nMelody {i+1}:")
        print(" -> ".join(melody))
        
        # Save as MIDI
        midi_filename = f"outputs/melodies/melody_{i+1}.mid"
        save_melody_as_midi(melody, midi_filename)
        print(f"Saved as {midi_filename}")

if __name__ == "__main__":
    main()