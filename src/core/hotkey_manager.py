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
            try:
                self.listener.stop()
            except Exception as e:
                print(f"Error stopping previous hotkey listener: {e}")
            self.listener = None
        
        # Build new hotkey mapping
        hotkey_mapping = {}
        
        if self.start_stop_hotkey and self.on_start_stop_pressed:
            formatted_key = self._format_hotkey(self.start_stop_hotkey)
            if formatted_key:
                hotkey_mapping[formatted_key] = self._on_start_stop_activated
                print(f"Registered start/stop hotkey: {formatted_key}")
            
        if self.play_hotkey and self.on_play_pressed:
            formatted_key = self._format_hotkey(self.play_hotkey)
            if formatted_key:
                hotkey_mapping[formatted_key] = self._on_play_activated
                print(f"Registered play hotkey: {formatted_key}")
        
        # Start new listener if we have hotkeys
        if hotkey_mapping:
            try:
                print(f"Starting hotkey listener with mappings: {list(hotkey_mapping.keys())}")
                self.listener = keyboard.GlobalHotKeys(hotkey_mapping)
                self.listener.start()
                self.is_active = True
                print("Hotkey listener started successfully")
                return True
            except Exception as e:
                print(f"Error setting up hotkeys: {e}")
                import traceback
                traceback.print_exc()
                self.is_active = False
                return False
        else:
            print("No hotkeys to register")
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
            lower_part = part.strip().lower()
            if lower_part in ['ctrl', 'control']:
                formatted_parts.append('<ctrl>')
            elif lower_part in ['alt', 'menu']:
                formatted_parts.append('<alt>')
            elif lower_part in ['shift']:
                formatted_parts.append('<shift>')
            elif lower_part in ['cmd', 'win', 'windows']:
                formatted_parts.append('<cmd>')
            elif lower_part.startswith('f') and lower_part[1:].isdigit():
                # Function key - ensure it's in proper format
                formatted_parts.append(f'<{lower_part}>')
            elif len(lower_part) == 1 and lower_part.isalnum():
                # Single character key
                formatted_parts.append(lower_part)
            elif lower_part in ['space', 'tab', 'enter', 'return', 'escape', 'esc', 'backspace', 'delete', 'insert', 'home', 'end', 'page_up', 'page_down', 'up', 'down', 'left', 'right']:
                # Special keys
                key_mapping = {
                    'return': 'enter',
                    'esc': 'escape',
                    'page_up': 'page_up',
                    'page_down': 'page_down'
                }
                mapped_key = key_mapping.get(lower_part, lower_part)
                formatted_parts.append(f'<{mapped_key}>')
            else:
                # Try as-is for other keys
                formatted_parts.append(lower_part)
        
        result = '+'.join(formatted_parts)
        print(f"Hotkey format conversion: '{hotkey_str}' -> '{result}'")  # Debug output
        return result
    
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
