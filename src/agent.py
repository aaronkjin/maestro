import numpy as np
import random
from typing import Dict, List, Tuple

class QLearningAgent:
    def __init__(self, n_actions: int, learning_rate: float = 0.1, 
                 gamma: float = 0.99, epsilon_start: float = 0.3):
        self.q_table: Dict[str, np.ndarray] = {}
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon_start
        
        self.good_patterns: List[List[Tuple[int, Duration]]] = []
        self.min_pattern_reward = 5
        
        self.current_measure_actions = []
        self.measure_rewards = []
    

    def get_action(self, state: str, env_info: Dict) -> int:
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.n_actions)
        
        current_beat = env_info['current_beat']
        beat_in_measure = current_beat % 4
        
        if beat_in_measure == 0 and self.good_patterns and np.random.random() > self.epsilon:
            pattern = np.random.choice(len(self.good_patterns))
            return self.good_patterns[pattern][0][0]
        
        # Epsilon-greedy selection w/ rhythm constraints
        if np.random.random() < self.epsilon:
            valid_actions = [
                action for action in range(self.n_actions)
                if env_info['is_valid_duration'](action)
            ]

            return np.random.choice(valid_actions) if valid_actions else 0
        
        else:
            q_values = self.q_table[state].copy()

            for action in range(self.n_actions):
                if not env_info['is_valid_duration'](action):
                    q_values[action] = -np.inf

            return np.argmax(q_values)
    

    def update(self, state: str, action: int, reward: float, 
               next_state: str, done: bool, env_info: Dict):

        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.n_actions)
        
        current_q = self.q_table[state][action]
        next_max_q = np.max(self.q_table[next_state]) if not done else 0
        new_q = current_q + self.lr * (reward + self.gamma * next_max_q - current_q)
        self.q_table[state][action] = new_q
        
        self.current_measure_actions.append((action, env_info['current_duration']))
        self.measure_rewards.append(reward)
        
        if env_info['measure_complete']:
            measure_reward = sum(self.measure_rewards)

            if measure_reward > self.min_pattern_reward:
                if self.current_measure_actions not in self.good_patterns:
                    self.good_patterns.append(self.current_measure_actions.copy())
            
            self.current_measure_actions = []
            self.measure_rewards = []
    
    
    def decay_epsilon(self):
        self.epsilon = max(0.01, self.epsilon * random.uniform(0.995, 0.999))