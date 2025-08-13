"""
Global hotkey management.
"""

import threading
from typing import Callable, Optional, Dict
from pynput import keyboard

from utils.key_utils import normalize_hotkey_string, validate_hotkey_string


class HotkeyManager:
    """Manages global hotkeys for the application."""
    
    def __init__(self):
        self.listener: Optional[keyboard.GlobalHotKeys] = None
        self.hotkeys: Dict[str, Callable] = {}
        self.is_active = False
        
        # Current hotkey assignments
        self.start_stop_hotkey = ""
        self.play_hotkey = ""
        
        # Callbacks
        self.on_start_stop_pressed: Optional[Callable] = None
        self.on_play_pressed: Optional[Callable] = None
    
    def set_start_stop_hotkey(self, hotkey_str: str) -> bool:
        """Set the start/stop recording hotkey."""
        normalized = normalize_hotkey_string(hotkey_str)
        
        if not validate_hotkey_string(normalized):
            return False
            
        self.start_stop_hotkey = normalized
        self._update_hotkeys()
        return True
    
    def set_play_hotkey(self, hotkey_str: str) -> bool:
        """Set the play hotkey."""
        normalized = normalize_hotkey_string(hotkey_str)
        
        if not validate_hotkey_string(normalized):
            return False
            
        self.play_hotkey = normalized
        self._update_hotkeys()
        return True
    
    def _update_hotkeys(self):
        """Update the global hotkey listener with current assignments."""
        # Stop existing listener
        if self.listener:
            self.listener.stop()
            self.listener = None
        
        # Build new hotkey mapping
        hotkey_mapping = {}
        
        if self.start_stop_hotkey and self.on_start_stop_pressed:
            hotkey_mapping[self._format_hotkey(self.start_stop_hotkey)] = self._on_start_stop_activated
            
        if self.play_hotkey and self.on_play_pressed:
            hotkey_mapping[self._format_hotkey(self.play_hotkey)] = self._on_play_activated
        
        # Start new listener if we have hotkeys
        if hotkey_mapping:
            try:
                self.listener = keyboard.GlobalHotKeys(hotkey_mapping)
                self.listener.start()
                self.is_active = True
                return True
            except Exception as e:
                print(f"Error setting up hotkeys: {e}")
                self.is_active = False
                return False
        else:
            self.is_active = False
            return True
    
    def _format_hotkey(self, hotkey_str: str) -> str:
        """Format hotkey string for pynput GlobalHotKeys."""
        if not hotkey_str:
            return ""
            
        # Convert our format to pynput format
        # Example: "Ctrl+F1" -> "<ctrl>+<f1>"
        parts = hotkey_str.split('+')
        formatted_parts = []
        
        for part in parts:
            lower_part = part.lower()
            if lower_part in ['ctrl', 'alt', 'shift']:
                formatted_parts.append(f'<{lower_part}>')
            elif lower_part.startswith('f') and lower_part[1:].isdigit():
                # Function key
                formatted_parts.append(f'<{lower_part}>')
            else:
                # Regular key
                formatted_parts.append(lower_part)
        
        return '+'.join(formatted_parts)
    
    def _on_start_stop_activated(self):
        """Handle start/stop hotkey activation."""
        if self.on_start_stop_pressed:
            # Run callback in separate thread to avoid blocking
            threading.Thread(
                target=self.on_start_stop_pressed,
                daemon=True
            ).start()
    
    def _on_play_activated(self):
        """Handle play hotkey activation."""
        if self.on_play_pressed:
            # Run callback in separate thread to avoid blocking
            threading.Thread(
                target=self.on_play_pressed,
                daemon=True
            ).start()
    
    def start(self) -> bool:
        """Start the hotkey manager."""
        return self._update_hotkeys()
    
    def stop(self):
        """Stop the hotkey manager."""
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.is_active = False
    
    def cleanup(self):
        """Clean up resources."""
        self.stop()
    
    def get_active_hotkeys(self) -> Dict[str, str]:
        """Get currently active hotkeys."""
        return {
            'start_stop': self.start_stop_hotkey,
            'play': self.play_hotkey
        }
    
    def is_hotkey_available(self, hotkey_str: str) -> bool:
        """Check if a hotkey string is available (not in use)."""
        normalized = normalize_hotkey_string(hotkey_str)
        return (normalized != self.start_stop_hotkey and 
                normalized != self.play_hotkey)
