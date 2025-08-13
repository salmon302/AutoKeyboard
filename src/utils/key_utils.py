"""
Utility functions for key handling and mapping.
"""

from typing import Dict, Set, Optional
from pynput import keyboard


# Key name mappings for display
KEY_DISPLAY_NAMES = {
    keyboard.Key.ctrl_l: "Left Ctrl",
    keyboard.Key.ctrl_r: "Right Ctrl", 
    keyboard.Key.alt_l: "Left Alt",
    keyboard.Key.alt_r: "Right Alt",
    keyboard.Key.shift_l: "Left Shift",
    keyboard.Key.shift_r: "Right Shift",
    keyboard.Key.cmd: "Windows",
    keyboard.Key.space: "Space",
    keyboard.Key.tab: "Tab",
    keyboard.Key.caps_lock: "Caps Lock",
    keyboard.Key.enter: "Enter",
    keyboard.Key.backspace: "Backspace",
    keyboard.Key.delete: "Delete",
    keyboard.Key.insert: "Insert",
    keyboard.Key.home: "Home",
    keyboard.Key.end: "End",
    keyboard.Key.page_up: "Page Up",
    keyboard.Key.page_down: "Page Down",
    keyboard.Key.up: "Up Arrow",
    keyboard.Key.down: "Down Arrow",
    keyboard.Key.left: "Left Arrow",
    keyboard.Key.right: "Right Arrow",
    keyboard.Key.esc: "Escape",
    keyboard.Key.print_screen: "Print Screen",
    keyboard.Key.scroll_lock: "Scroll Lock",
    keyboard.Key.pause: "Pause",
    keyboard.Key.menu: "Menu",
    keyboard.Key.num_lock: "Num Lock",
}

# Function keys
for i in range(1, 25):
    KEY_DISPLAY_NAMES[getattr(keyboard.Key, f'f{i}')] = f'F{i}'

# Numpad keys
NUMPAD_KEYS = {
    keyboard.Key.insert: "Numpad 0",
    keyboard.Key.end: "Numpad 1", 
    keyboard.Key.down: "Numpad 2",
    keyboard.Key.page_down: "Numpad 3",
    keyboard.Key.left: "Numpad 4",
    # Add more numpad mappings as needed
}

# Common hotkey options for dropdowns
HOTKEY_OPTIONS = [
    "None", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
    "Ctrl+F1", "Ctrl+F2", "Ctrl+F3", "Ctrl+F4", "Ctrl+F5", "Ctrl+F6",
    "Alt+F1", "Alt+F2", "Alt+F3", "Alt+F4", "Alt+F5", "Alt+F6",
    "Shift+F1", "Shift+F2", "Shift+F3", "Shift+F4", "Shift+F5", "Shift+F6"
]


def get_key_display_name(key) -> str:
    """Get display name for a key."""
    if hasattr(key, 'char') and key.char:
        # Regular character key
        return key.char.upper()
    elif key in KEY_DISPLAY_NAMES:
        # Special key
        return KEY_DISPLAY_NAMES[key]
    else:
        # Fallback to string representation
        return str(key).replace('Key.', '').replace('_', ' ').title()


def get_key_code(key) -> str:
    """Get a consistent string code for a key."""
    if hasattr(key, 'char') and key.char:
        return f"char:{key.char}"
    else:
        return f"key:{key.name}"


def parse_key_code(key_code: str):
    """Parse a key code back to a key object."""
    if key_code.startswith("char:"):
        return keyboard.KeyCode.from_char(key_code[5:])
    elif key_code.startswith("key:"):
        key_name = key_code[4:]
        try:
            return getattr(keyboard.Key, key_name)
        except AttributeError:
            return None
    return None


def is_modifier_key(key) -> bool:
    """Check if a key is a modifier key."""
    modifier_keys = {
        keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
        keyboard.Key.alt_l, keyboard.Key.alt_r,
        keyboard.Key.shift_l, keyboard.Key.shift_r,
        keyboard.Key.cmd
    }
    return key in modifier_keys


def normalize_hotkey_string(hotkey_str: str) -> str:
    """Normalize hotkey string format."""
    if not hotkey_str or hotkey_str == "None":
        return ""
    
    # Split by + and normalize each part
    parts = [part.strip().title() for part in hotkey_str.split('+')]
    return '+'.join(parts)


def validate_hotkey_string(hotkey_str: str) -> bool:
    """Validate if hotkey string is valid."""
    if not hotkey_str or hotkey_str == "None":
        return True
        
    try:
        # Try to parse the hotkey string
        parts = hotkey_str.split('+')
        if len(parts) > 3:  # Too many modifiers
            return False
            
        # Check if last part is a valid key
        key_part = parts[-1].lower()
        if key_part.startswith('f') and key_part[1:].isdigit():
            # Function key
            return True
        elif len(key_part) == 1 and key_part.isalnum():
            # Single character
            return True
        elif key_part in ['space', 'tab', 'enter', 'escape', 'backspace']:
            # Common special keys
            return True
            
        return False
        
    except Exception:
        return False
