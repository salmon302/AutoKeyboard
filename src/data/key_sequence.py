"""
Data models for key sequences and actions.
"""

import time
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ActionType(Enum):
    """Types of recorded actions."""
    KEY_PRESS = "key_press"
    KEY_RELEASE = "key_release"
    DELAY = "delay"


@dataclass
class KeyAction:
    """Represents a single key action (press/release) with timing."""
    action_type: ActionType
    key: str
    timestamp: float
    duration: float = 0.0  # For key hold duration
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'action_type': self.action_type.value,
            'key': self.key,
            'timestamp': self.timestamp,
            'duration': self.duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KeyAction':
        """Create from dictionary."""
        return cls(
            action_type=ActionType(data['action_type']),
            key=data['key'],
            timestamp=data['timestamp'],
            duration=data.get('duration', 0.0)
        )


class KeySequence:
    """Manages a sequence of key actions."""
    
    def __init__(self, name: str = ""):
        self.name = name
        self.actions: List[KeyAction] = []
        self.created_at = time.time()
        self.modified_at = time.time()
    
    def add_action(self, action: KeyAction):
        """Add a key action to the sequence."""
        self.actions.append(action)
        self.modified_at = time.time()
    
    def clear(self):
        """Clear all actions."""
        self.actions.clear()
        self.modified_at = time.time()
    
    def get_duration(self) -> float:
        """Get total duration of the sequence."""
        if not self.actions:
            return 0.0
        return self.actions[-1].timestamp - self.actions[0].timestamp
    
    def get_key_count(self) -> int:
        """Get number of key press actions."""
        return len([a for a in self.actions if a.action_type == ActionType.KEY_PRESS])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'actions': [action.to_dict() for action in self.actions],
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KeySequence':
        """Create from dictionary."""
        sequence = cls(data.get('name', ''))
        sequence.actions = [KeyAction.from_dict(action_data) 
                          for action_data in data.get('actions', [])]
        sequence.created_at = data.get('created_at', time.time())
        sequence.modified_at = data.get('modified_at', time.time())
        return sequence
    
    def __len__(self) -> int:
        """Return number of actions."""
        return len(self.actions)
    
    def __bool__(self) -> bool:
        """Return True if sequence has actions."""
        return len(self.actions) > 0
