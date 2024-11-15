from typing import List
from src.environment import MusicEnvironment
from src.agent import QLearningAgent

def train_agent(env: MusicEnvironment, agent: QLearningAgent, 
                n_episodes: int = 1000) -> List[float]:
    """Train the Q-learning agent."""
    episode_rewards = []
    
    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.get_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.update(state, action, reward, next_state, done)
            
            state = next_state
            total_reward += reward
        
        episode_rewards.append(total_reward)
        
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}, Total Reward: {total_reward}")
    
    return episode_rewards

def generate_melody(env: MusicEnvironment, agent: QLearningAgent) -> List[str]:
    """Generate a melody using the trained agent."""
    state = env.reset()
    melody = []
    done = False
    
    while not done:
        action = agent.get_action(state)
        note = env.idx_to_note[action]
        melody.append(note)
        
        state, _, done, _ = env.step(action)
    
    return melody