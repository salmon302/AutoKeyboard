"""
Key recording functionality.
"""

import time
import threading
from typing import Callable, Optional, Set
from pynput import keyboard

from data.key_sequence import KeySequence, KeyAction, ActionType
from utils.key_utils import get_key_code, get_key_display_name


class KeyRecorder:
    """Handles recording of key presses and releases."""
    
    def __init__(self):
        self.is_recording = False
        self.current_sequence = KeySequence()
        self.listener: Optional[keyboard.Listener] = None
        self.start_time = 0.0
        self.pressed_keys: Set[str] = set()
        
        # Callbacks
        self.on_recording_started: Optional[Callable] = None
        self.on_recording_stopped: Optional[Callable] = None
        self.on_key_recorded: Optional[Callable[[KeyAction], None]] = None
    
    def start_recording(self) -> bool:
        """Start recording key presses."""
        if self.is_recording:
            return False
            
        try:
            # Clear previous sequence
            self.current_sequence.clear()
            self.pressed_keys.clear()
            
            # Start listener
            self.listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            self.listener.start()
            
            # Mark recording state
            self.is_recording = True
            self.start_time = time.time()
            
            # Notify callback
            if self.on_recording_started:
                self.on_recording_started()
                
            return True
            
        except Exception as e:
            print(f"Error starting recording: {e}")
            return False
    
    def stop_recording(self) -> KeySequence:
        """Stop recording and return the recorded sequence."""
        if not self.is_recording:
            return self.current_sequence
            
        try:
            # Stop listener
            if self.listener:
                self.listener.stop()
                self.listener = None
                
            # Mark recording state
            self.is_recording = False
            
            # Notify callback
            if self.on_recording_stopped:
                self.on_recording_stopped()
                
            return self.current_sequence
            
        except Exception as e:
            print(f"Error stopping recording: {e}")
            return self.current_sequence
    
    def _on_key_press(self, key):
        """Handle key press events."""
        if not self.is_recording:
            return
            
        try:
            key_code = get_key_code(key)
            current_time = time.time()
            relative_time = current_time - self.start_time
            
            # Check if key is already pressed (avoid key repeat)
            if key_code in self.pressed_keys:
                return
                
            self.pressed_keys.add(key_code)
            
            # Create key action
            action = KeyAction(
                action_type=ActionType.KEY_PRESS,
                key=key_code,
                timestamp=relative_time
            )
            
            # Add to sequence
            self.current_sequence.add_action(action)
            
            # Notify callback
            if self.on_key_recorded:
                self.on_key_recorded(action)
                
        except Exception as e:
            print(f"Error handling key press: {e}")
    
    def _on_key_release(self, key):
        """Handle key release events."""
        if not self.is_recording:
            return
            
        try:
            key_code = get_key_code(key)
            current_time = time.time()
            relative_time = current_time - self.start_time
            
            # Remove from pressed keys
            self.pressed_keys.discard(key_code)
            
            # Find corresponding press action to calculate duration
            press_action = None
            for action in reversed(self.current_sequence.actions):
                if (action.action_type == ActionType.KEY_PRESS and 
                    action.key == key_code and action.duration == 0.0):
                    press_action = action
                    break
            
            # Update press action with duration
            if press_action:
                press_action.duration = relative_time - press_action.timestamp
            
            # Create release action
            action = KeyAction(
                action_type=ActionType.KEY_RELEASE,
                key=key_code,
                timestamp=relative_time
            )
            
            # Add to sequence
            self.current_sequence.add_action(action)
            
        except Exception as e:
            print(f"Error handling key release: {e}")
    
    def get_recorded_sequence(self) -> KeySequence:
        """Get the currently recorded sequence."""
        return self.current_sequence
    
    def clear_sequence(self):
        """Clear the recorded sequence."""
        self.current_sequence.clear()
    
    def get_recording_duration(self) -> float:
        """Get the current recording duration in seconds."""
        if not self.is_recording:
            return 0.0
        return time.time() - self.start_time
