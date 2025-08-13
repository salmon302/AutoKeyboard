import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from data.key_sequence import KeySequence, KeyAction, ActionType


class TestKeySequence(unittest.TestCase):
    """Test cases for KeySequence class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sequence = KeySequence()
    
    def test_should_initialize_empty_sequence(self):
        """Test that a new sequence initializes empty."""
        self.assertEqual(len(self.sequence.actions), 0)
        self.assertEqual(self.sequence.get_duration(), 0.0)
    
    def test_should_add_action_successfully(self):
        """Test adding an action to the sequence."""
        action = KeyAction(ActionType.KEY_PRESS, "a", 0.0)
        self.sequence.add_action(action)
        
        self.assertEqual(len(self.sequence.actions), 1)
        self.assertEqual(self.sequence.actions[0], action)
    
    def test_should_clear_all_actions(self):
        """Test clearing all actions from sequence."""
        # Add some actions
        self.sequence.add_action(KeyAction(ActionType.KEY_PRESS, "a", 0.0))
        self.sequence.add_action(KeyAction(ActionType.KEY_PRESS, "b", 0.1))
        
        # Clear and verify
        self.sequence.clear()
        self.assertEqual(len(self.sequence.actions), 0)
    
    def test_should_calculate_duration_correctly(self):
        """Test duration calculation."""
        self.sequence.add_action(KeyAction(ActionType.KEY_PRESS, "a", 0.0))
        self.sequence.add_action(KeyAction(ActionType.KEY_PRESS, "b", 1.5))
        
        self.assertEqual(self.sequence.get_duration(), 1.5)
    
    def test_should_convert_to_string_representation(self):
        """Test string representation of sequence."""
        self.sequence.add_action(KeyAction(ActionType.KEY_PRESS, "a", 0.0))
        self.sequence.add_action(KeyAction(ActionType.KEY_PRESS, "b", 0.1))
        
        result = self.sequence.to_string()
        self.assertIn("KEY: a", result)
        self.assertIn("KEY: b", result)


class TestKeyAction(unittest.TestCase):
    """Test cases for KeyAction class."""
    
    def test_should_create_key_action(self):
        """Test creating a key action."""
        action = KeyAction(ActionType.KEY_PRESS, "test_key", 1.0, 0.5)
        
        self.assertEqual(action.action_type, ActionType.KEY_PRESS)
        self.assertEqual(action.key, "test_key")
        self.assertEqual(action.timestamp, 1.0)
        self.assertEqual(action.duration, 0.5)
    
    def test_should_have_string_representation(self):
        """Test string representation of action."""
        action = KeyAction(ActionType.KEY_PRESS, "a", 0.0)
        result = str(action)
        
        self.assertIn("KEY_PRESS", result)
        self.assertIn("a", result)


if __name__ == '__main__':
    unittest.main()
