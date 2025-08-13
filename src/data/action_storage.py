"""
Action storage and script file management.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

from data.key_sequence import KeySequence, KeyAction, ActionType


class ActionStorage:
    """Manages saving and loading of recorded actions and scripts."""
    
    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            self.storage_dir = os.path.join(os.path.expanduser("~"), ".autokeyboard", "scripts")
        else:
            self.storage_dir = storage_dir
            
        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def save_sequence(self, sequence: KeySequence, filename: str = None) -> bool:
        """Save a key sequence to file."""
        try:
            if filename is None:
                # Generate filename from timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sequence_{timestamp}.json"
            
            if not filename.endswith('.json'):
                filename += '.json'
            
            filepath = os.path.join(self.storage_dir, filename)
            
            # Convert sequence to dictionary
            data = {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'sequence': sequence.to_dict()
            }
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving sequence: {e}")
            return False
    
    def load_sequence(self, filename: str) -> Optional[KeySequence]:
        """Load a key sequence from file."""
        try:
            if not filename.endswith('.json'):
                filename += '.json'
                
            filepath = os.path.join(self.storage_dir, filename)
            
            if not os.path.exists(filepath):
                return None
            
            # Load from file
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract sequence data
            sequence_data = data.get('sequence', {})
            sequence = KeySequence.from_dict(sequence_data)
            
            return sequence
            
        except Exception as e:
            print(f"Error loading sequence: {e}")
            return None
    
    def list_saved_sequences(self) -> List[Dict[str, str]]:
        """List all saved sequences with metadata."""
        sequences = []
        
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.storage_dir, filename)
                    
                    try:
                        # Get file info
                        stat = os.stat(filepath)
                        modified = datetime.fromtimestamp(stat.st_mtime)
                        
                        # Try to load metadata
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        sequence_data = data.get('sequence', {})
                        name = sequence_data.get('name', filename[:-5])  # Remove .json
                        action_count = len(sequence_data.get('actions', []))
                        
                        sequences.append({
                            'filename': filename,
                            'name': name,
                            'action_count': action_count,
                            'modified': modified.strftime("%Y-%m-%d %H:%M"),
                            'created': data.get('created', 'Unknown')
                        })
                        
                    except Exception as e:
                        # If we can't read the file, include basic info
                        sequences.append({
                            'filename': filename,
                            'name': filename[:-5],
                            'action_count': 0,
                            'modified': modified.strftime("%Y-%m-%d %H:%M"),
                            'created': 'Unknown',
                            'error': str(e)
                        })
            
            # Sort by modification date (newest first)
            sequences.sort(key=lambda x: x['modified'], reverse=True)
            
        except Exception as e:
            print(f"Error listing sequences: {e}")
        
        return sequences
    
    def delete_sequence(self, filename: str) -> bool:
        """Delete a saved sequence."""
        try:
            if not filename.endswith('.json'):
                filename += '.json'
                
            filepath = os.path.join(self.storage_dir, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error deleting sequence: {e}")
            return False
    
    def export_sequence_to_script(self, sequence: KeySequence, filepath: str) -> bool:
        """Export a sequence as a human-readable script file."""
        try:
            script_lines = [
                f"# AutoKeyboard Script - {sequence.name}",
                f"# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"# Actions: {len(sequence.actions)}",
                "",
            ]
            
            for action in sequence.actions:
                if action.action_type == ActionType.KEY_PRESS:
                    # Try to get human-readable key name
                    key_name = self._get_readable_key_name(action.key)
                    script_lines.append(f"KEY: {key_name}")
                elif action.action_type == ActionType.DELAY:
                    delay_ms = int(action.duration * 1000)
                    script_lines.append(f"DELAY: {delay_ms}")
                elif action.action_type == ActionType.KEY_RELEASE:
                    # Skip key releases in script format
                    continue
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(script_lines))
            
            return True
            
        except Exception as e:
            print(f"Error exporting script: {e}")
            return False
    
    def import_script_to_sequence(self, filepath: str) -> Optional[KeySequence]:
        """Import a script file as a key sequence."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse script content
            lines = content.split('\n')
            sequence = KeySequence(os.path.basename(filepath))
            timestamp = 0.0
            
            for line in lines:
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                if line.upper().startswith('KEY:'):
                    key_part = line[4:].strip()
                    action = KeyAction(
                        action_type=ActionType.KEY_PRESS,
                        key=self._parse_script_key(key_part),
                        timestamp=timestamp
                    )
                    sequence.add_action(action)
                    timestamp += 0.1
                    
                elif line.upper().startswith('DELAY:'):
                    delay_part = line[6:].strip()
                    delay_ms = int(delay_part)
                    
                    timestamp += delay_ms / 1000.0
                    
                    action = KeyAction(
                        action_type=ActionType.DELAY,
                        key="",
                        timestamp=timestamp,
                        duration=delay_ms / 1000.0
                    )
                    sequence.add_action(action)
            
            return sequence
            
        except Exception as e:
            print(f"Error importing script: {e}")
            return None
    
    def _get_readable_key_name(self, key_code: str) -> str:
        """Convert key code to readable name."""
        if key_code.startswith("char:"):
            return key_code[5:]
        elif key_code.startswith("key:"):
            key_name = key_code[4:]
            # Capitalize special keys
            return key_name.replace('_', ' ').title()
        elif key_code.startswith("combo:"):
            return key_code[6:]
        else:
            return key_code
    
    def _parse_script_key(self, key_string: str) -> str:
        """Parse script key string to key code."""
        # Handle combinations
        if '+' in key_string:
            return f"combo:{key_string}"
        
        key_lower = key_string.lower()
        
        # Special keys mapping
        special_keys = {
            'enter': 'key:enter',
            'space': 'key:space',
            'tab': 'key:tab', 
            'escape': 'key:esc',
            'backspace': 'key:backspace',
            'delete': 'key:delete',
            'home': 'key:home',
            'end': 'key:end',
            'pageup': 'key:page_up',
            'pagedown': 'key:page_down',
            'up': 'key:up',
            'down': 'key:down',
            'left': 'key:left',
            'right': 'key:right'
        }
        
        if key_lower in special_keys:
            return special_keys[key_lower]
        elif key_lower.startswith('f') and key_lower[1:].isdigit():
            return f"key:f{key_lower[1:]}"
        elif len(key_string) == 1:
            return f"char:{key_string.lower()}"
        else:
            return f"char:{key_string}"
    
    def get_storage_directory(self) -> str:
        """Get the storage directory path."""
        return self.storage_dir
