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
        char = key_code[5:]
        return keyboard.KeyCode.from_char(char)
    elif key_code.startswith("key:"):
        key_name = key_code[4:]
        try:
            return getattr(keyboard.Key, key_name)
        except AttributeError:
            # Handle special numpad keys
            if key_name.startswith('num_'):
                numpad_mapping = {
                    'num_0': keyboard.KeyCode.from_vk(96),
                    'num_1': keyboard.KeyCode.from_vk(97),
                    'num_2': keyboard.KeyCode.from_vk(98),
                    'num_3': keyboard.KeyCode.from_vk(99),
                    'num_4': keyboard.KeyCode.from_vk(100),
                    'num_5': keyboard.KeyCode.from_vk(101),
                    'num_6': keyboard.KeyCode.from_vk(102),
                    'num_7': keyboard.KeyCode.from_vk(103),
                    'num_8': keyboard.KeyCode.from_vk(104),
                    'num_9': keyboard.KeyCode.from_vk(105),
                    'num_multiply': keyboard.KeyCode.from_vk(106),
                    'num_plus': keyboard.KeyCode.from_vk(107),
                    'num_minus': keyboard.KeyCode.from_vk(109),
                    'num_decimal': keyboard.KeyCode.from_vk(110),
                    'num_divide': keyboard.KeyCode.from_vk(111),
                    'num_enter': keyboard.KeyCode.from_vk(13),
                }
                return numpad_mapping.get(key_name)
            return None
    elif key_code.startswith("combo:"):
        # Handle key combinations
        combo_str = key_code[6:]
        # For combinations, we'll return a special tuple
        # This will need special handling in the player
        parts = combo_str.split('+')
        keys = []
        for part in parts:
            if hasattr(keyboard.Key, part):
                keys.append(getattr(keyboard.Key, part))
            elif len(part) == 1:
                keys.append(keyboard.KeyCode.from_char(part))
        return tuple(keys) if len(keys) > 1 else (keys[0] if keys else None)
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


def get_key_code_from_name(key_name: str) -> str:
    """Convert a key name to a key code for storage."""
    key_name = key_name.strip()
    
    # Handle single characters (letters, numbers, symbols)
    if len(key_name) == 1:
        if key_name.isalnum():
            return f"char:{key_name.lower()}"
        else:
            # Handle single character symbols
            return f"char:{key_name}"
    
    # Comprehensive special key mapping
    special_key_mapping = {
        # Navigation keys
        'space': 'key:space',
        'tab': 'key:tab', 
        'enter': 'key:enter',
        'return': 'key:enter',
        'escape': 'key:esc',
        'esc': 'key:esc',
        'backspace': 'key:backspace',
        'delete': 'key:delete',
        'insert': 'key:insert',
        'home': 'key:home',
        'end': 'key:end',
        'page up': 'key:page_up',
        'page down': 'key:page_down',
        'pageup': 'key:page_up',
        'pagedown': 'key:page_down',
        
        # Arrow keys
        'up arrow': 'key:up',
        'down arrow': 'key:down',
        'left arrow': 'key:left',
        'right arrow': 'key:right',
        'up': 'key:up',
        'down': 'key:down',
        'left': 'key:left',
        'right': 'key:right',
        
        # Modifier keys
        'ctrl': 'key:ctrl_l',
        'control': 'key:ctrl_l',
        'alt': 'key:alt_l',
        'shift': 'key:shift_l',
        'menu': 'key:alt_l',
        'windows': 'key:cmd',
        'win': 'key:cmd',
        'cmd': 'key:cmd',
        'left ctrl': 'key:ctrl_l',
        'right ctrl': 'key:ctrl_r',
        'left alt': 'key:alt_l', 
        'right alt': 'key:alt_r',
        'left shift': 'key:shift_l',
        'right shift': 'key:shift_r',
        
        # Lock keys
        'caps lock': 'key:caps_lock',
        'capslock': 'key:caps_lock',
        'num lock': 'key:num_lock',
        'numlock': 'key:num_lock',
        'scroll lock': 'key:scroll_lock',
        'scrolllock': 'key:scroll_lock',
        
        # System keys
        'print screen': 'key:print_screen',
        'printscreen': 'key:print_screen',
        'pause': 'key:pause',
        'break': 'key:pause',
        'menu': 'key:menu',
        
        # Numpad keys
        'numpad 0': 'key:num_0',
        'numpad 1': 'key:num_1',
        'numpad 2': 'key:num_2',
        'numpad 3': 'key:num_3',
        'numpad 4': 'key:num_4',
        'numpad 5': 'key:num_5',
        'numpad 6': 'key:num_6',
        'numpad 7': 'key:num_7',
        'numpad 8': 'key:num_8',
        'numpad 9': 'key:num_9',
        'numpad +': 'key:num_plus',
        'numpad -': 'key:num_minus',
        'numpad *': 'key:num_multiply',
        'numpad /': 'key:num_divide',
        'numpad .': 'key:num_decimal',
        'numpad enter': 'key:num_enter',
        
        # Symbol keys (for reference, though single chars are handled above)
        'minus': 'char:-',
        'equals': 'char:=',
        'plus': 'char:+',
        'underscore': 'char:_',
        'left bracket': 'char:[',
        'right bracket': 'char:]',
        'left brace': 'char:{',
        'right brace': 'char:}',
        'semicolon': 'char:;',
        'quote': 'char:\'',
        'double quote': 'char:"',
        'comma': 'char:,',
        'period': 'char:.',
        'slash': 'char:/',
        'backslash': 'char:\\',
        'backtick': 'char:`',
        'tilde': 'char:~',
        'exclamation': 'char:!',
        'at': 'char:@',
        'hash': 'char:#',
        'dollar': 'char:$',
        'percent': 'char:%',
        'caret': 'char:^',
        'ampersand': 'char:&',
        'asterisk': 'char:*',
        'left paren': 'char:(',
        'right paren': 'char:)',
        'question': 'char:?',
        'less than': 'char:<',
        'greater than': 'char:>',
        'pipe': 'char:|',
    }
    
    lower_name = key_name.lower()
    
    # Check special keys first
    if lower_name in special_key_mapping:
        return special_key_mapping[lower_name]
    
    # Handle function keys F1-F24
    if lower_name.startswith('f') and lower_name[1:].isdigit():
        return f"key:{lower_name}"
    
    # Handle combination keys (like "ctrl+a")
    if '+' in key_name:
        # This is a combination, handle each part
        parts = [part.strip() for part in key_name.split('+')]
        converted_parts = []
        for part in parts:
            part_code = get_key_code_from_name(part)
            if part_code.startswith('key:'):
                converted_parts.append(part_code[4:])
            elif part_code.startswith('char:'):
                converted_parts.append(part_code[5:])
            else:
                converted_parts.append(part.lower())
        return f"combo:{'+'.join(converted_parts)}"
    
    # Try to match against pynput Key attributes
    try:
        # Clean the name for pynput attribute lookup
        clean_name = lower_name.replace(' ', '_').replace('-', '_')
        # Test if this attribute exists in keyboard.Key
        test_key = getattr(keyboard.Key, clean_name)
        return f"key:{clean_name}"
    except AttributeError:
        pass
    
    # Default to character if single char, otherwise treat as special key
    if len(key_name) == 1:
        return f"char:{key_name.lower()}"
    else:
        # Try to map to a key name
        clean_name = lower_name.replace(' ', '_')
        return f"key:{clean_name}"


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
