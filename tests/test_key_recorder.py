import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from core.key_recorder import KeyRecorder
from data.key_sequence import KeySequence, ActionType


class TestKeyRecorder(unittest.TestCase):
    """Test cases for KeyRecorder class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.recorder = KeyRecorder()
    
    def test_should_initialize_with_default_state(self):
        """Test that recorder initializes with correct default state."""
        self.assertFalse(self.recorder.is_recording)
        self.assertIsInstance(self.recorder.current_sequence, KeySequence)
        self.assertIsNone(self.recorder.listener)
        self.assertEqual(len(self.recorder.pressed_keys), 0)
    
    @patch('core.key_recorder.keyboard.Listener')
    def test_should_start_recording_successfully(self, mock_listener_class):
        """Test starting recording."""
        mock_listener = MagicMock()
        mock_listener_class.return_value = mock_listener
        
        result = self.recorder.start_recording()
        
        self.assertTrue(result)
        self.assertTrue(self.recorder.is_recording)
        mock_listener.start.assert_called_once()
    
    def test_should_not_start_recording_when_already_recording(self):
        """Test that recording cannot be started when already recording."""
        self.recorder.is_recording = True
        
        result = self.recorder.start_recording()
        
        self.assertFalse(result)
    
    def test_should_stop_recording_successfully(self):
        """Test stopping recording."""
        # Set up recording state
        mock_listener = MagicMock()
        self.recorder.listener = mock_listener
        self.recorder.is_recording = True
        
        result = self.recorder.stop_recording()
        
        self.assertFalse(self.recorder.is_recording)
        mock_listener.stop.assert_called_once()
        self.assertIsInstance(result, KeySequence)
    
    def test_should_handle_stop_when_not_recording(self):
        """Test stopping when not recording."""
        result = self.recorder.stop_recording()
        
        self.assertFalse(self.recorder.is_recording)
        self.assertIsInstance(result, KeySequence)
    
    def test_should_clear_sequence(self):
        """Test clearing recorded sequence."""
        # Add some mock data
        self.recorder.current_sequence.add_action(
            Mock(action_type=ActionType.KEY_PRESS, key="a", timestamp=0.0)
        )
        
        self.recorder.clear_sequence()
        
        self.assertEqual(len(self.recorder.current_sequence.actions), 0)
    
    def test_should_get_recorded_sequence(self):
        """Test getting recorded sequence."""
        result = self.recorder.get_recorded_sequence()
        
        self.assertIs(result, self.recorder.current_sequence)
    
    def test_should_get_recording_duration_when_not_recording(self):
        """Test getting duration when not recording."""
        duration = self.recorder.get_recording_duration()
        
        self.assertEqual(duration, 0.0)
    
    @patch('core.key_recorder.time.time')
    def test_should_get_recording_duration_when_recording(self, mock_time):
        """Test getting duration when recording."""
        mock_time.side_effect = [100.0, 105.5]  # start_time, current_time
        
        self.recorder.is_recording = True
        self.recorder.start_time = mock_time()
        duration = self.recorder.get_recording_duration()
        
        self.assertEqual(duration, 5.5)
    
    def test_should_set_callbacks(self):
        """Test setting callback functions."""
        started_callback = Mock()
        stopped_callback = Mock()
        recorded_callback = Mock()
        
        self.recorder.on_recording_started = started_callback
        self.recorder.on_recording_stopped = stopped_callback
        self.recorder.on_key_recorded = recorded_callback
        
        self.assertIs(self.recorder.on_recording_started, started_callback)
        self.assertIs(self.recorder.on_recording_stopped, stopped_callback)
        self.assertIs(self.recorder.on_key_recorded, recorded_callback)


if __name__ == '__main__':
    unittest.main()
