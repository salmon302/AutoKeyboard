"""
Application settings management.
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class AppSettings:
    """Application settings data class."""
    
    # Hotkey settings
    start_stop_hotkey: str = "F1"
    play_hotkey: str = "F2"
    
    # Timing settings
    time_between_presses: int = 500  # milliseconds
    repeat_count: int = 1
    repeat_continuously: bool = False
    disable_countdown_timer: bool = False
    
    # Window settings
    window_x: int = 100
    window_y: int = 100
    
    # Recording settings
    record_key_holds: bool = True
    min_hold_duration: int = 100  # milliseconds


class Settings:
    """Manages application settings persistence."""
    
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = settings_file
        self.settings = AppSettings()
        self._settings_dir = os.path.join(os.path.expanduser("~"), ".autokeyboard")
        self._settings_path = os.path.join(self._settings_dir, settings_file)
    
    def load(self) -> bool:
        """Load settings from file."""
        try:
            if not os.path.exists(self._settings_path):
                return False
                
            with open(self._settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Update settings with loaded data
            for key, value in data.items():
                if hasattr(self.settings, key):
                    setattr(self.settings, key, value)
                    
            return True
            
        except Exception as e:
            print(f"Error loading settings: {e}")
            return False
    
    def save(self) -> bool:
        """Save settings to file."""
        try:
            # Create settings directory if it doesn't exist
            os.makedirs(self._settings_dir, exist_ok=True)
            
            # Convert settings to dictionary
            data = asdict(self.settings)
            
            # Save to file
            with open(self._settings_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return getattr(self.settings, key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Set a setting value."""
        try:
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
                return True
            return False
        except Exception:
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = AppSettings()
    
    def get_settings_dict(self) -> Dict[str, Any]:
        """Get all settings as dictionary."""
        return asdict(self.settings)
