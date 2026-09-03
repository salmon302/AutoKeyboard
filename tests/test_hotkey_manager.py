# SPDX-License-Identifier: MIT
"""
Test cases for HotkeyManager class.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from core.hotkey_manager import HotkeyManager
from utils.key_utils import normalize_hotkey_string


class TestHotkeyManager(unittest.TestCase):
    """Test cases for HotkeyManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('core.hotkey_manager.keyboard.GlobalHotKeys'):
            self.manager = HotkeyManager()
            self.manager.listener = None
            self.manager.is_active = False
    
    def test_should_initialize_with_default_state(self):
        """Test that manager initializes with correct default state."""
        self.assertFalse(self.manager.is_active)
        self.assertEqual(self.manager.start_stop_hotkey, "")
        self.assertEqual(self.manager.play_hotkey, "")
        self.assertIsNone(self.manager.on_start_stop_pressed)
        self.assertIsNone(self.manager.on_play_pressed)
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    def test_set_start_stop_hotkey_registers_hotkey(self, mock_ghg):
        """Test that set_start_stop_hotkey validates and registers the hotkey."""
        mock_listener_instance = MagicMock()
        mock_ghg.return_value = mock_listener_instance
        
        result = self.manager.set_start_stop_hotkey("F1")
        
        self.assertTrue(result)
        self.assertEqual(self.manager.start_stop_hotkey, "F1")
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    def test_set_play_hotkey_registers_hotkey(self, mock_ghg):
        """Test that set_play_hotkey validates and registers the hotkey."""
        mock_listener_instance = MagicMock()
        mock_ghg.return_value = mock_listener_instance
        
        result = self.manager.set_play_hotkey("F2")
        
        self.assertTrue(result)
        self.assertEqual(self.manager.play_hotkey, "F2")
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    def test_should_reject_invalid_hotkey(self, mock_ghg):
        """Test that invalid hotkey strings are rejected."""
        result = self.manager.set_start_stop_hotkey("NotAValidKey")
        
        self.assertFalse(result)
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    def test_update_hotkeys_stops_existing_listener_before_starting_new(self, mock_ghg):
        """Test that _update_hotkeys stops the old listener before creating a new one.
        
        This is the core of the 'cannot always reassign hotkey' bug fix:
        the old listener must be fully stopped (joined) before the new one
        is created, otherwise the system-level hook may conflict.
        """
        # Set up a mock listener with join
        old_listener = MagicMock()
        self.manager.listener = old_listener
        self.manager.start_stop_hotkey = "F1"
        self.manager.on_start_stop_pressed = Mock()
        
        mock_listener_instance = MagicMock()
        mock_ghg.return_value = mock_listener_instance
        
        # Call _update_hotkeys - this should stop+join the old listener
        self.manager._update_hotkeys()
        
        # Verify old listener was stopped and joined
        old_listener.stop.assert_called_once()
        old_listener.join.assert_called_once_with(timeout=2.0)
        
        # Verify new listener was created
        self.assertIsNotNone(self.manager.listener)
        mock_listener_instance.start.assert_called_once()
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    def test_update_hotkeys_retries_on_failure(self, mock_ghg):
        """Test that _update_hotkeys retries when listener creation fails."""
        self.manager.start_stop_hotkey = "F1"
        self.manager.on_start_stop_pressed = Mock()
        
        # Make GlobalHotKeys fail on first two attempts, succeed on third
        mock_ghg.side_effect = [
            Exception("Hook registration failed"),
            Exception("Hook registration failed"),
            MagicMock()
        ]
        
        result = self.manager._update_hotkeys()
        
        # Should have retried and eventually succeeded
        self.assertTrue(mock_ghg.call_count >= 2)
        self.assertTrue(result)
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    def test_update_hotkeys_fails_after_max_retries(self, mock_ghg):
        """Test that _update_hotkeys gives up after max retries."""
        self.manager.start_stop_hotkey = "F1"
        self.manager.on_start_stop_pressed = Mock()
        
        mock_ghg.side_effect = Exception("Hook registration failed")
        
        result = self.manager._update_hotkeys()
        
        self.assertFalse(result)
        self.assertFalse(self.manager.is_active)
        # Should have tried 3 times
        self.assertEqual(mock_ghg.call_count, 3)
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    @patch('core.hotkey_manager.time.sleep')
    def test_update_hotkeys_stops_old_listener_with_join(self, mock_sleep, mock_ghg):
        """Regression test: old listener must be joined (not just stopped)."""
        old_listener = MagicMock()
        self.manager.listener = old_listener
        self.manager.start_stop_hotkey = "F1"
        self.manager.on_start_stop_pressed = Mock()
        
        mock_listener_instance = MagicMock()
        mock_ghg.return_value = mock_listener_instance
        
        self.manager._update_hotkeys()
        
        # The fix: join must be called on the old listener
        self.assertTrue(old_listener.join.called)
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    def test_stop_method_joins_listener(self, mock_ghg):
        """Test that stop() properly joins the listener thread."""
        old_listener = MagicMock()
        self.manager.listener = old_listener
        self.manager.is_active = True
        
        self.manager.stop()
        
        old_listener.stop.assert_called_once()
        old_listener.join.assert_called_once_with(timeout=2.0)
        self.assertFalse(self.manager.is_active)
        self.assertIsNone(self.manager.listener)
    
    def test_get_active_hotkeys(self):
        """Test getting active hotkeys."""
        self.manager.start_stop_hotkey = "F1"
        self.manager.play_hotkey = "F2"
        
        result = self.manager.get_active_hotkeys()
        
        self.assertEqual(result['start_stop'], "F1")
        self.assertEqual(result['play'], "F2")
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    def test_reassign_hotkey_multiple_times(self, mock_ghg):
        """Test that a hotkey can be reassigned multiple times without failure.
        
        This directly tests the 'cannot always reassign' bug: calling
        set_start_stop_hotkey multiple times should work every time.
        """
        self.manager.on_start_stop_pressed = Mock()
        
        for hotkey in ["F1", "F2", "F3", "Ctrl+F1", "Alt+F2"]:
            mock_listener = MagicMock()
            mock_ghg.return_value = mock_listener
            
            result = self.manager.set_start_stop_hotkey(hotkey)
            self.assertTrue(result, f"Failed to set hotkey: {hotkey}")
            self.assertEqual(self.manager.start_stop_hotkey, normalize_hotkey_string(hotkey))
    
    def test_is_hotkey_available(self):
        """Test checking if a hotkey is available."""
        self.manager.start_stop_hotkey = "F1"
        self.manager.play_hotkey = "F2"
        
        # F1 and F2 are in use
        self.assertFalse(self.manager.is_hotkey_available("F1"))
        self.assertFalse(self.manager.is_hotkey_available("F2"))
        
        # F3 is available
        self.assertTrue(self.manager.is_hotkey_available("F3"))
    
    @patch('core.hotkey_manager.keyboard.GlobalHotKeys')
    def test_update_hotkeys_no_hotkeys_registered(self, mock_ghg):
        """Test that update_hotkeys handles empty hotkey state gracefully."""
        result = self.manager._update_hotkeys()
        
        self.assertTrue(result)
        self.assertFalse(self.manager.is_active)
        mock_ghg.assert_not_called()


if __name__ == '__main__':
    unittest.main()
