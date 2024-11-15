from typing import List
from .environment import MusicEnvironment, Note, Duration
from .agent import QLearningAgent


def train_agent(env: MusicEnvironment, agent: QLearningAgent, 
                n_episodes: int = 2000) -> List[float]:
    episode_rewards = []
    
    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            env_info = {
                'current_beat': env.current_beat,
                'current_measure': env.current_measure,
                'is_valid_duration': lambda action: env._is_valid_duration(env.action_to_note[action].duration),
                'current_duration': env.action_to_note[action].duration if 'action' in locals() else None,
                'measure_complete': env._is_measure_complete()
            }
            
            action = agent.get_action(state, env_info)
            next_state, reward, done, _ = env.step(action)
            
            env_info['measure_complete'] = env._is_measure_complete()
            agent.update(state, action, reward, next_state, done, env_info)
            
            state = next_state
            total_reward += reward
        
        episode_rewards.append(total_reward)
        agent.decay_epsilon()
        
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}, Total Reward: {total_reward:.2f}, "
                  f"Epsilon: {agent.epsilon:.3f}")
    
    return episode_rewards


def generate_melody(env: MusicEnvironment, agent: QLearningAgent) -> List[Note]:
    state = env.reset()
    melody = []
    done = False
    
    while not done:
        env_info = {
            'current_beat': env.current_beat,
            'current_measure': env.current_measure,
            'is_valid_duration': lambda action: env._is_valid_duration(env.action_to_note[action].duration),
            'current_duration': env.action_to_note[action].duration if 'action' in locals() else None,
            'measure_complete': env._is_measure_complete()
        }
        
        action = agent.get_action(state, env_info)
        note = env.action_to_note[action]
        melody.append(note)
        
        state, _, done, _ = env.step(action)
    
    return melody