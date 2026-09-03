import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from data.key_sequence import KeySequence, KeyAction, ActionType


class TestMainWindowStopRecording(unittest.TestCase):
    """Test cases for the Stop Recording button functionality."""
    
    def test_stop_recording_calls_recorder_stop(self):
        """Test that _on_stop_recording calls recorder.stop_recording() when recording."""
        from gui.main_window import MainWindow
        
        # Create mock dependencies
        mock_root = MagicMock()
        mock_recorder = MagicMock()
        mock_recorder.is_recording = False  # Will be set by state
        mock_player = MagicMock()
        mock_hotkey_manager = MagicMock()
        mock_settings = MagicMock()
        mock_settings.get.side_effect = lambda key, default=None: {
            'start_stop_hotkey': 'F1',
            'play_hotkey': 'F2',
            'time_between_presses': 500,
            'repeat_count': 1,
            'repeat_continuously': False,
            'disable_countdown_timer': False,
        }.get(key, default)
        
        # We need to test the handler logic without full GUI instantiation
        # Create a partial MainWindow-like object
        with patch.object(MainWindow, '_create_widgets'), \
             patch.object(MainWindow, '_layout_widgets'), \
             patch.object(MainWindow, '_setup_bindings'):
            window = MainWindow(mock_root, mock_recorder, mock_player, 
                               mock_hotkey_manager, mock_settings)
            window.is_recording = True
            
            # Call the stop recording handler
            window._on_stop_recording()
            
            # Verify stop_recording was called
            mock_recorder.stop_recording.assert_called_once()
    
    def test_stop_recording_does_nothing_when_not_recording(self):
        """Test that _on_stop_recording does nothing when not recording."""
        from gui.main_window import MainWindow
        
        mock_root = MagicMock()
        mock_recorder = MagicMock()
        mock_player = MagicMock()
        mock_hotkey_manager = MagicMock()
        mock_settings = MagicMock()
        mock_settings.get.side_effect = lambda key, default=None: {
            'start_stop_hotkey': 'F1',
            'play_hotkey': 'F2',
            'time_between_presses': 500,
            'repeat_count': 1,
            'repeat_continuously': False,
            'disable_countdown_timer': False,
        }.get(key, default)
        
        with patch.object(MainWindow, '_create_widgets'), \
             patch.object(MainWindow, '_layout_widgets'), \
             patch.object(MainWindow, '_setup_bindings'):
            window = MainWindow(mock_root, mock_recorder, mock_player,
                               mock_hotkey_manager, mock_settings)
            window.is_recording = False
            
            # Call the stop recording handler
            window._on_stop_recording()
            
            # Verify stop_recording was NOT called
            mock_recorder.stop_recording.assert_not_called()


class TestMainWindowDeleteAction(unittest.TestCase):
    """Test cases for the Delete key action removal functionality."""
    
    def _create_mock_window(self):
        """Create a MainWindow instance with mocked dependencies for testing."""
        from gui.main_window import MainWindow
        
        mock_root = MagicMock()
        mock_recorder = MagicMock()
        mock_recorder.current_sequence = KeySequence()
        mock_recorder.get_recorded_sequence = lambda: mock_recorder.current_sequence
        mock_player = MagicMock()
        mock_hotkey_manager = MagicMock()
        mock_settings = MagicMock()
        mock_settings.get.side_effect = lambda key, default=None: {
            'start_stop_hotkey': 'F1',
            'play_hotkey': 'F2',
            'time_between_presses': 500,
            'repeat_count': 1,
            'repeat_continuously': False,
            'disable_countdown_timer': False,
        }.get(key, default)
        
        # Mock the listbox
        mock_listbox = MagicMock()
        mock_listbox.curselection.return_value = ()
        mock_listbox.size.return_value = 0
        
        with patch.object(MainWindow, '_create_widgets'), \
             patch.object(MainWindow, '_layout_widgets'), \
             patch.object(MainWindow, '_setup_bindings'):
            window = MainWindow(mock_root, mock_recorder, mock_player,
                               mock_hotkey_manager, mock_settings)
            window.action_listbox = mock_listbox
            window._listbox_action_indices = []
            window.status_var = Mock()
            
            return window, mock_recorder, mock_listbox
    
    def test_delete_action_no_selection_does_nothing(self):
        """Test that deleting with no selection does nothing."""
        window, mock_recorder, mock_listbox = self._create_mock_window()
        
        mock_listbox.curselection.return_value = ()
        
        window._on_delete_action()
        
        # Sequence should be unchanged
        self.assertEqual(len(mock_recorder.current_sequence.actions), 0)
    
    def test_delete_action_removes_key_press_and_release(self):
        """Test that deleting a key press action also removes its key release."""
        window, mock_recorder, mock_listbox = self._create_mock_window()
        
        # Set up a sequence: KEY_PRESS 'a', KEY_RELEASE 'a', KEY_PRESS 'b', KEY_RELEASE 'b'
        mock_recorder.current_sequence.actions = [
            KeyAction(ActionType.KEY_PRESS, "char:a", 0.0),
            KeyAction(ActionType.KEY_RELEASE, "char:a", 0.1),
            KeyAction(ActionType.KEY_PRESS, "char:b", 0.2),
            KeyAction(ActionType.KEY_RELEASE, "char:b", 0.3),
        ]
        
        # Set up the listbox with 2 items (only KEY_PRESS and DELAY are shown)
        mock_listbox.curselection.return_value = (0,)  # Select first item
        mock_listbox.size.return_value = 2
        window._listbox_action_indices = [0, 2]  # Listbox idx 0 -> seq idx 0, idx 1 -> seq idx 2
        
        # Mock the insert/delete/update methods
        mock_listbox.delete = MagicMock()
        mock_listbox.insert = MagicMock()
        mock_listbox.clear = MagicMock()
        
        with patch.object(window, '_update_action_list_from_sequence'):
            window._on_delete_action()
        
        # Should have removed 2 actions (KEY_PRESS 'a' and KEY_RELEASE 'a')
        self.assertEqual(len(mock_recorder.current_sequence.actions), 2)
        remaining_keys = [a.key for a in mock_recorder.current_sequence.actions]
        self.assertIn("char:b", remaining_keys)
        self.assertNotIn("char:a", remaining_keys)
    
    def test_delete_action_removes_delay(self):
        """Test that deleting a delay action only removes that delay."""
        window, mock_recorder, mock_listbox = self._create_mock_window()
        
        # Set up a sequence: KEY_PRESS, DELAY, KEY_PRESS
        mock_recorder.current_sequence.actions = [
            KeyAction(ActionType.KEY_PRESS, "char:a", 0.0),
            KeyAction(ActionType.DELAY, "", 0.0, 1.0),
            KeyAction(ActionType.KEY_PRESS, "char:b", 1.1),
        ]
        
        # The listbox shows: "Key: a" (idx 0 -> seq 0), "Delay: 1000ms" (idx 1 -> seq 1), "Key: b" (idx 2 -> seq 2)
        mock_listbox.curselection.return_value = (1,)  # Select delay (second item)
        mock_listbox.size.return_value = 3
        window._listbox_action_indices = [0, 1, 2]
        
        mock_listbox.delete = MagicMock()
        mock_listbox.insert = MagicMock()
        
        with patch.object(window, '_update_action_list_from_sequence'):
            window._on_delete_action()
        
        # Should have removed only 1 action (the delay)
        self.assertEqual(len(mock_recorder.current_sequence.actions), 2)
        remaining = [a.action_type for a in mock_recorder.current_sequence.actions]
        self.assertEqual(remaining.count(ActionType.KEY_PRESS), 2)
        self.assertNotIn(ActionType.DELAY, remaining)
    
    def test_delete_action_out_of_sync_rebuilds_mapping(self):
        """Test that delete gracefully handles out-of-sync mapping."""
        window, mock_recorder, mock_listbox = self._create_mock_window()
        
        # Listbox has selection at index 5, but mapping only has 3 entries
        mock_listbox.curselection.return_value = (5,)
        mock_listbox.size.return_value = 5
        window._listbox_action_indices = [0, 1, 2]  # Only 3 entries
        
        mock_listbox.delete = MagicMock()
        mock_listbox.insert = MagicMock()
        
        with patch.object(window, '_update_action_list_from_sequence') as mock_rebuild:
            window._on_delete_action()
            # Should have called rebuild to repopulate the mapping
            mock_rebuild.assert_called_once()


if __name__ == '__main__':
    unittest.main()
