import numpy as np
import random
from typing import Dict

class QLearningAgent:
    def __init__(self, n_actions: int, learning_rate: float = 0.1, 
                 gamma: float = 0.95, epsilon: float = 0.1):
        self.q_table: Dict[str, np.ndarray] = {}
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
    
    def get_action(self, state: str) -> int:
        """Select action using epsilon-greedy policy."""
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.n_actions)
        
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return np.argmax(self.q_table[state])
    
    def update(self, state: str, action: int, reward: float, 
               next_state: str, done: bool):
        """Update Q-value for state-action pair."""
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.n_actions)
        
        current_q = self.q_table[state][action]
        next_max_q = np.max(self.q_table[next_state]) if not done else 0
        new_q = current_q + self.lr * (reward + self.gamma * next_max_q - current_q)
        self.q_table[state][action] = new_q