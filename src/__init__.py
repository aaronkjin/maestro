from .environment import MusicEnvironment, Note, Duration
from .agent import QLearningAgent
from .train import train_agent, generate_melody
from .utils import save_melody_as_midi

__all__ = [
    'MusicEnvironment',
    'QLearningAgent',
    'train_agent',
    'generate_melody',
    'save_melody_as_midi',
    'Note',
    'Duration'
]

__all__ = ['MusicEnvironment', 'QLearningAgent', 'train_agent', 
           'generate_melody', 'save_melody_as_midi']