"""
Key playback functionality.
"""

import time
import threading
from typing import Callable, Optional, List
from pynput import keyboard
from pynput.keyboard import Controller

from data.key_sequence import KeySequence, KeyAction, ActionType
from utils.key_utils import parse_key_code


class KeyPlayer:
    """Handles playback of recorded key sequences."""
    
    def __init__(self):
        self.is_playing = False
        self.controller = Controller()
        self.playback_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
        # Playback settings
        self.time_between_presses = 500  # milliseconds
        self.repeat_count = 1
        self.repeat_continuously = False
        
        # Callbacks
        self.on_playback_started: Optional[Callable] = None
        self.on_playback_stopped: Optional[Callable] = None
        self.on_playback_progress: Optional[Callable[[int, int], None]] = None
    
    def start_playback(self, sequence: KeySequence) -> bool:
        """Start playing back a key sequence."""
        if self.is_playing or not sequence:
            return False
            
        try:
            # Reset stop event
            self.stop_event.clear()
            
            # Start playback in separate thread
            self.playback_thread = threading.Thread(
                target=self._playback_worker,
                args=(sequence,),
                daemon=True
            )
            
            self.is_playing = True
            self.playback_thread.start()
            
            # Notify callback
            if self.on_playback_started:
                self.on_playback_started()
                
            return True
            
        except Exception as e:
            print(f"Error starting playback: {e}")
            self.is_playing = False
            return False
    
    def stop_playback(self):
        """Stop current playback."""
        if not self.is_playing:
            return
            
        # Signal stop
        self.stop_event.set()
        
        # Wait for thread to finish
        if self.playback_thread and self.playback_thread.is_alive():
            self.playback_thread.join(timeout=1.0)
            
        self.is_playing = False
        
        # Notify callback
        if self.on_playback_stopped:
            self.on_playback_stopped()
    
    def _playback_worker(self, sequence: KeySequence):
        """Worker thread for key playback."""
        try:
            repetitions = self.repeat_count if not self.repeat_continuously else -1
            current_rep = 0
            
            while (repetitions == -1 or current_rep < repetitions) and not self.stop_event.is_set():
                # Play sequence once
                self._play_sequence_once(sequence)
                
                current_rep += 1
                
                # Update progress
                if self.on_playback_progress and repetitions > 0:
                    self.on_playback_progress(current_rep, repetitions)
                
                # Wait between repetitions (except for last one)
                if (repetitions == -1 or current_rep < repetitions) and not self.stop_event.is_set():
                    self._wait_interruptible(self.time_between_presses / 1000.0)
                    
        except Exception as e:
            print(f"Error in playback worker: {e}")
            
        finally:
            self.is_playing = False
            if self.on_playback_stopped:
                self.on_playback_stopped()
    
    def _play_sequence_once(self, sequence: KeySequence):
        """Play a sequence once."""
        if not sequence.actions:
            return
            
        # Get only key press actions for simple playback
        key_presses = [action for action in sequence.actions 
                      if action.action_type == ActionType.KEY_PRESS]
        
        for i, action in enumerate(key_presses):
            if self.stop_event.is_set():
                break
                
            try:
                # Parse key from stored code
                key = parse_key_code(action.key)
                if key is None:
                    continue
                    
                # Press and release key
                self.controller.press(key)
                time.sleep(0.01)  # Small delay for key registration
                self.controller.release(key)
                
                # Wait before next key (except for last one)
                if i < len(key_presses) - 1:
                    self._wait_interruptible(self.time_between_presses / 1000.0)
                    
            except Exception as e:
                print(f"Error playing key {action.key}: {e}")
                continue
    
    def _wait_interruptible(self, seconds: float):
        """Wait for specified seconds, but can be interrupted."""
        self.stop_event.wait(timeout=seconds)
    
    def set_timing(self, time_between_presses: int):
        """Set time between key presses in milliseconds."""
        self.time_between_presses = max(1, time_between_presses)
    
    def set_repeat_count(self, count: int):
        """Set number of repetitions."""
        self.repeat_count = max(1, count)
        self.repeat_continuously = False
    
    def set_repeat_continuously(self, continuous: bool):
        """Set continuous repeat mode."""
        self.repeat_continuously = continuous
    
    def get_playback_settings(self) -> dict:
        """Get current playback settings."""
        return {
            'time_between_presses': self.time_between_presses,
            'repeat_count': self.repeat_count,
            'repeat_continuously': self.repeat_continuously
        }
