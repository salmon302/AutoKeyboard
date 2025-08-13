"""
Script editor window for editing recorded key sequences.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional, Callable, List
import json

from data.key_sequence import KeySequence, KeyAction, ActionType
from data.action_storage import ActionStorage
from utils.key_utils import get_key_display_name, parse_key_code, get_key_code, HOTKEY_OPTIONS


class ScriptEditorWindow:
    """Window for editing recorded key sequences as scripts."""
    
    def __init__(self, parent: tk.Tk, sequence: KeySequence, on_save_callback: Optional[Callable[[KeySequence], None]] = None):
        self.parent = parent
        self.original_sequence = sequence
        self.on_save_callback = on_save_callback
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Script Editor - AutoKeyboard Presser")
        self.window.geometry("700x500")
        self.window.resizable(True, True)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self._center_window()
        
        # Create GUI
        self._create_widgets()
        self._layout_widgets()
        self._setup_bindings()
        
        # Load current sequence
        self._load_sequence()
        
        # Focus on editor
        self.editor.focus_set()
    
    def _center_window(self):
        """Center the window on the parent."""
        self.window.update_idletasks()
        
        # Get dimensions
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate position
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        
        # Main frame
        self.main_frame = ttk.Frame(self.window, padding="10")
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.title_label = ttk.Label(
            self.header_frame,
            text="Script Editor",
            font=("Arial", 12, "bold")
        )
        self.info_label = ttk.Label(
            self.header_frame,
            text="Edit your recorded key sequence. Each line represents one key action.",
            font=("Arial", 9)
        )
        
        # Toolbar
        self.toolbar_frame = ttk.Frame(self.main_frame)
        
        self.add_key_button = ttk.Button(
            self.toolbar_frame,
            text="Add Key",
            command=self._add_key_dialog
        )
        
        self.add_delay_button = ttk.Button(
            self.toolbar_frame,
            text="Add Delay",
            command=self._add_delay_dialog
        )
        
        self.clear_button = ttk.Button(
            self.toolbar_frame,
            text="Clear All",
            command=self._clear_script
        )
        
        self.load_template_button = ttk.Button(
            self.toolbar_frame,
            text="Load Template",
            command=self._load_template_dialog
        )
        
        # Editor frame
        self.editor_frame = ttk.LabelFrame(self.main_frame, text="Script Content", padding="5")
        
        # Text editor with scrollbar
        self.editor_text_frame = ttk.Frame(self.editor_frame)
        
        self.editor = scrolledtext.ScrolledText(
            self.editor_text_frame,
            height=15,
            width=70,
            font=("Consolas", 10),
            wrap=tk.NONE
        )
        
        # Status and help
        self.status_frame = ttk.Frame(self.main_frame)
        
        self.help_text = tk.Text(
            self.status_frame,
            height=4,
            width=70,
            font=("Arial", 8),
            bg="#f0f0f0",
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        
        self.validate_button = ttk.Button(
            self.button_frame,
            text="Validate Script",
            command=self._validate_script
        )
        
        self.save_button = ttk.Button(
            self.button_frame,
            text="Save & Apply",
            command=self._save_script
        )
        
        self.cancel_button = ttk.Button(
            self.button_frame,
            text="Cancel",
            command=self._cancel
        )
    
    def _layout_widgets(self):
        """Layout all widgets."""
        
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # Header
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.title_label.grid(row=0, column=0, sticky="w")
        self.info_label.grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        # Toolbar
        self.toolbar_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.add_key_button.grid(row=0, column=0, padx=(0, 5))
        self.add_delay_button.grid(row=0, column=1, padx=(0, 5))
        self.clear_button.grid(row=0, column=2, padx=(0, 5))
        self.load_template_button.grid(row=0, column=3, padx=(0, 5))
        
        # Editor
        self.editor_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.main_frame.rowconfigure(2, weight=1)
        
        self.editor_text_frame.grid(row=0, column=0, sticky="nsew")
        self.editor_frame.columnconfigure(0, weight=1)
        self.editor_frame.rowconfigure(0, weight=1)
        
        self.editor.grid(row=0, column=0, sticky="nsew")
        self.editor_text_frame.columnconfigure(0, weight=1)
        self.editor_text_frame.rowconfigure(0, weight=1)
        
        # Status/Help
        self.status_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self.help_text.grid(row=0, column=0, sticky="ew")
        self.status_frame.columnconfigure(0, weight=1)
        
        # Buttons
        self.button_frame.grid(row=4, column=0, sticky="ew")
        self.button_frame.columnconfigure(2, weight=1)  # Spacer
        
        self.validate_button.grid(row=0, column=0, padx=(0, 5))
        self.save_button.grid(row=0, column=3, padx=(0, 5))
        self.cancel_button.grid(row=0, column=4)
        
        # Load help text
        self._load_help_text()
    
    def _setup_bindings(self):
        """Setup event bindings."""
        self.window.protocol("WM_DELETE_WINDOW", self._cancel)
        self.window.bind("<Control-s>", lambda e: self._save_script())
        self.window.bind("<Escape>", lambda e: self._cancel())
        self.window.bind("<F5>", lambda e: self._validate_script())
    
    def _load_help_text(self):
        """Load help text into the help area."""
        help_content = """Script Format: Each line represents one action. Examples:
KEY: a                    - Press and release key 'a'
KEY: F1                   - Press function key F1
KEY: ctrl+c               - Press Ctrl+C combination
DELAY: 1000               - Wait 1000 milliseconds (1 second)"""
        
        self.help_text.config(state=tk.NORMAL)
        self.help_text.delete(1.0, tk.END)
        self.help_text.insert(1.0, help_content)
        self.help_text.config(state=tk.DISABLED)
    
    def _load_sequence(self):
        """Load the current sequence into the editor."""
        if not self.original_sequence or not self.original_sequence.actions:
            self._load_template()
            return
        
        script_lines = []
        
        for action in self.original_sequence.actions:
            if action.action_type == ActionType.KEY_PRESS:
                try:
                    key = parse_key_code(action.key)
                    if key:
                        key_name = get_key_display_name(key)
                        script_lines.append(f"KEY: {key_name}")
                    else:
                        script_lines.append(f"KEY: {action.key}")
                except:
                    script_lines.append(f"KEY: {action.key}")
            elif action.action_type == ActionType.DELAY:
                delay_ms = int(action.duration * 1000)
                script_lines.append(f"DELAY: {delay_ms}")
        
        script_content = "\n".join(script_lines)
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, script_content)
    
    def _load_template(self):
        """Load a basic template."""
        template = """# AutoKeyboard Script Template
# Each line represents one action
# Examples:

KEY: a
DELAY: 500
KEY: b
DELAY: 500
KEY: Enter

# Available key formats:
# - Single keys: a, b, 1, 2, etc.
# - Function keys: F1, F2, F3, etc.
# - Special keys: Enter, Space, Tab, Escape, etc.
# - Combinations: ctrl+c, alt+tab, shift+a, etc.
# - Delays: DELAY: 1000 (milliseconds)"""
        
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, template)
    
    def _add_key_dialog(self):
        """Show dialog to add a key."""
        dialog = AddKeyDialog(self.window, self._insert_key)
    
    def _add_delay_dialog(self):
        """Show dialog to add a delay."""
        dialog = AddDelayDialog(self.window, self._insert_delay)
    
    def _insert_key(self, key_text: str):
        """Insert a key at cursor position."""
        cursor_pos = self.editor.index(tk.INSERT)
        self.editor.insert(cursor_pos, f"KEY: {key_text}\n")
    
    def _insert_delay(self, delay_ms: int):
        """Insert a delay at cursor position."""
        cursor_pos = self.editor.index(tk.INSERT)
        self.editor.insert(cursor_pos, f"DELAY: {delay_ms}\n")
    
    def _clear_script(self):
        """Clear the entire script."""
        if messagebox.askyesno("Clear Script", "Are you sure you want to clear the entire script?"):
            self.editor.delete(1.0, tk.END)
    
    def _load_template_dialog(self):
        """Show template selection dialog."""
        templates = {
            "Basic Template": self._load_template,
            "Hello World": lambda: self._load_preset("hello_world"),
            "Copy Paste": lambda: self._load_preset("copy_paste"),
            "Alt Tab": lambda: self._load_preset("alt_tab")
        }
        
        dialog = TemplateDialog(self.window, templates)
    
    def _load_preset(self, preset_name: str):
        """Load a preset script."""
        presets = {
            "hello_world": """KEY: h
KEY: e
KEY: l
KEY: l
KEY: o
KEY: Space
KEY: w
KEY: o
KEY: r
KEY: l
KEY: d""",
            "copy_paste": """KEY: ctrl+a
DELAY: 100
KEY: ctrl+c
DELAY: 500
KEY: ctrl+v""",
            "alt_tab": """KEY: alt+tab
DELAY: 1000
KEY: Enter"""
        }
        
        if preset_name in presets:
            self.editor.delete(1.0, tk.END)
            self.editor.insert(1.0, presets[preset_name])
    
    def _validate_script(self):
        """Validate the script syntax."""
        try:
            sequence = self._parse_script()
            if sequence:
                count = len([a for a in sequence.actions if a.action_type == ActionType.KEY_PRESS])
                messagebox.showinfo(
                    "Validation Successful",
                    f"Script is valid!\n\nFound {count} key actions and {len(sequence.actions) - count} other actions."
                )
                return True
        except Exception as e:
            messagebox.showerror("Validation Error", f"Script validation failed:\n\n{str(e)}")
            return False
    
    def _parse_script(self) -> Optional[KeySequence]:
        """Parse the script content into a KeySequence."""
        content = self.editor.get(1.0, tk.END).strip()
        if not content:
            return None
        
        lines = content.split('\n')
        sequence = KeySequence("Edited Script")
        timestamp = 0.0
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            try:
                if line.upper().startswith('KEY:'):
                    # Parse key action
                    key_part = line[4:].strip()
                    if not key_part:
                        raise ValueError(f"Empty key specification on line {line_num}")
                    
                    # Try to create a key action
                    action = KeyAction(
                        action_type=ActionType.KEY_PRESS,
                        key=self._parse_key_string(key_part),
                        timestamp=timestamp
                    )
                    sequence.add_action(action)
                    timestamp += 0.1  # Small increment between keys
                    
                elif line.upper().startswith('DELAY:'):
                    # Parse delay action
                    delay_part = line[6:].strip()
                    if not delay_part:
                        raise ValueError(f"Empty delay specification on line {line_num}")
                    
                    delay_ms = int(delay_part)
                    if delay_ms < 0:
                        raise ValueError(f"Negative delay not allowed on line {line_num}")
                    
                    # Add delay to timestamp for next action
                    timestamp += delay_ms / 1000.0
                    
                    # Create delay action
                    action = KeyAction(
                        action_type=ActionType.DELAY,
                        key="",
                        timestamp=timestamp,
                        duration=delay_ms / 1000.0
                    )
                    sequence.add_action(action)
                    
                else:
                    raise ValueError(f"Unknown command on line {line_num}: {line}")
                    
            except ValueError as e:
                raise ValueError(f"Line {line_num}: {str(e)}")
            except Exception as e:
                raise ValueError(f"Line {line_num}: Unexpected error - {str(e)}")
        
        return sequence
    
    def _parse_key_string(self, key_string: str) -> str:
        """Parse a key string and return a key code."""
        # Handle combinations like ctrl+c, alt+tab, etc.
        if '+' in key_string:
            parts = [part.strip().lower() for part in key_string.split('+')]
            # For now, just return the string as-is
            # In a full implementation, you'd parse modifiers properly
            return f"combo:{key_string}"
        else:
            # Single key
            key_lower = key_string.lower()
            
            # Map common special keys
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
                # Function key
                return f"key:f{key_lower[1:]}"
            elif len(key_string) == 1:
                # Single character
                return f"char:{key_string.lower()}"
            else:
                # Default to character
                return f"char:{key_string}"
    
    def _save_script(self):
        """Save the script and apply changes."""
        try:
            sequence = self._parse_script()
            if sequence:
                if self.on_save_callback:
                    self.on_save_callback(sequence)
                self.window.destroy()
            else:
                messagebox.showwarning("Empty Script", "The script is empty. Please add some actions.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Cannot save script:\n\n{str(e)}")
    
    def _cancel(self):
        """Cancel editing and close window."""
        if self.editor.get(1.0, tk.END).strip():
            if messagebox.askyesno("Cancel", "Are you sure you want to cancel? Any unsaved changes will be lost."):
                self.window.destroy()
        else:
            self.window.destroy()


class AddKeyDialog:
    """Dialog for adding a key to the script."""
    
    def __init__(self, parent: tk.Toplevel, callback: Callable[[str], None]):
        self.callback = callback
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Key")
        self.dialog.geometry("350x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self._center_dialog(parent)
        
        # Create widgets
        self._create_widgets()
        
        # Focus
        self.key_entry.focus_set()
    
    def _center_dialog(self, parent):
        """Center dialog on parent."""
        self.dialog.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (350 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (200 // 2)
        self.dialog.geometry(f"350x200+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        frame = ttk.Frame(self.dialog, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Key input
        ttk.Label(frame, text="Key to add:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.key_var = tk.StringVar()
        self.key_entry = ttk.Entry(frame, textvariable=self.key_var, width=30)
        self.key_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Examples
        examples_text = """Examples:
• Single keys: a, b, 1, 2, Enter, Space, Tab
• Function keys: F1, F2, F3
• Combinations: ctrl+c, alt+tab, shift+a"""
        
        ttk.Label(frame, text=examples_text, font=("Arial", 8)).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(button_frame, text="Add", command=self._add_key).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=2)
        
        # Bindings
        self.key_entry.bind("<Return>", lambda e: self._add_key())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
    
    def _add_key(self):
        """Add the key."""
        key_text = self.key_var.get().strip()
        if key_text:
            self.callback(key_text)
            self.dialog.destroy()


class AddDelayDialog:
    """Dialog for adding a delay to the script."""
    
    def __init__(self, parent: tk.Toplevel, callback: Callable[[int], None]):
        self.callback = callback
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Delay")
        self.dialog.geometry("300x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self._center_dialog(parent)
        
        # Create widgets
        self._create_widgets()
        
        # Focus
        self.delay_spinbox.focus_set()
    
    def _center_dialog(self, parent):
        """Center dialog on parent."""
        self.dialog.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (300 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (150 // 2)
        self.dialog.geometry(f"300x150+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        frame = ttk.Frame(self.dialog, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Delay input
        ttk.Label(frame, text="Delay (milliseconds):").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.delay_var = tk.IntVar(value=1000)
        self.delay_spinbox = ttk.Spinbox(
            frame, 
            from_=1, 
            to=60000, 
            textvariable=self.delay_var,
            width=20
        )
        self.delay_spinbox.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(button_frame, text="Add", command=self._add_delay).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=2)
        
        # Bindings
        self.delay_spinbox.bind("<Return>", lambda e: self._add_delay())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
    
    def _add_delay(self):
        """Add the delay."""
        delay_ms = self.delay_var.get()
        if delay_ms > 0:
            self.callback(delay_ms)
            self.dialog.destroy()


class TemplateDialog:
    """Dialog for selecting script templates."""
    
    def __init__(self, parent: tk.Toplevel, templates: dict):
        self.templates = templates
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Load Template")
        self.dialog.geometry("400x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self._center_dialog(parent)
        
        # Create widgets
        self._create_widgets()
    
    def _center_dialog(self, parent):
        """Center dialog on parent."""
        self.dialog.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (250 // 2)
        self.dialog.geometry(f"400x250+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        frame = ttk.Frame(self.dialog, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        
        ttk.Label(frame, text="Select a template:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )
        
        # Template list
        self.template_listbox = tk.Listbox(frame, height=8)
        for template_name in self.templates.keys():
            self.template_listbox.insert(tk.END, template_name)
        self.template_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(button_frame, text="Load", command=self._load_template).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=2)
        
        # Bindings
        self.template_listbox.bind("<Double-Button-1>", lambda e: self._load_template())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
        
        # Select first item
        if self.template_listbox.size() > 0:
            self.template_listbox.selection_set(0)
    
    def _load_template(self):
        """Load the selected template."""
        selection = self.template_listbox.curselection()
        if selection:
            template_name = self.template_listbox.get(selection[0])
            if template_name in self.templates:
                self.templates[template_name]()
                self.dialog.destroy()


class ScriptSaveDialog:
    """Dialog for saving scripts."""
    
    def __init__(self, parent: tk.Tk, storage: ActionStorage, sequence: KeySequence, 
                 callback: Callable[[bool, str], None]):
        self.storage = storage
        self.sequence = sequence
        self.callback = callback
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Save Script")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self._center_dialog(parent)
        
        # Create widgets
        self._create_widgets()
        
        # Focus on filename entry
        self.filename_entry.focus_set()
        self.filename_entry.select_range(0, tk.END)
    
    def _center_dialog(self, parent):
        """Center dialog on parent."""
        self.dialog.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        frame = ttk.Frame(self.dialog, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Title
        ttk.Label(frame, text="Save Script", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )
        
        # Filename input
        ttk.Label(frame, text="Filename:").grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        # Default filename based on current date/time
        import datetime
        default_name = f"script_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.filename_var = tk.StringVar(value=default_name)
        self.filename_entry = ttk.Entry(frame, textvariable=self.filename_var, width=40)
        self.filename_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        ttk.Label(frame, text="(Extension .json will be added automatically)", 
                 font=("Arial", 8)).grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Script info
        key_count = len([a for a in self.sequence.actions if a.action_type == ActionType.KEY_PRESS])
        total_count = len(self.sequence.actions)
        
        info_text = f"Actions to save: {key_count} keys, {total_count} total actions"
        ttk.Label(frame, text=info_text, font=("Arial", 9)).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(button_frame, text="Save", command=self._save_script).grid(
            row=0, column=1, padx=(0, 5)
        )
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).grid(
            row=0, column=2
        )
        
        # Bindings
        self.filename_entry.bind("<Return>", lambda e: self._save_script())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
    
    def _save_script(self):
        """Save the script."""
        filename = self.filename_var.get().strip()
        if not filename:
            messagebox.showerror("Error", "Please enter a filename.")
            return
        
        # Save the sequence
        success = self.storage.save_sequence(self.sequence, filename)
        
        # Call callback
        if self.callback:
            self.callback(success, filename)
        
        if success:
            self.dialog.destroy()


class ScriptLoadDialog:
    """Dialog for loading saved scripts."""
    
    def __init__(self, parent: tk.Tk, storage: ActionStorage, callback: Callable[[KeySequence], None]):
        self.storage = storage
        self.callback = callback
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Load Script")
        self.dialog.geometry("600x400")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self._center_dialog(parent)
        
        # Create widgets
        self._create_widgets()
        
        # Load script list
        self._refresh_script_list()
        
        # Focus on list
        if self.script_listbox.size() > 0:
            self.script_listbox.selection_set(0)
            self.script_listbox.focus_set()
    
    def _center_dialog(self, parent):
        """Center dialog on parent."""
        self.dialog.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (600 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (400 // 2)
        self.dialog.geometry(f"600x400+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        frame = ttk.Frame(self.dialog, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        
        # Title
        ttk.Label(frame, text="Load Saved Script", font=("Arial", 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 15)
        )
        
        # Script list with scrollbar
        list_frame = ttk.Frame(frame)
        list_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview for better display
        columns = ("name", "actions", "modified")
        self.script_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        # Configure columns
        self.script_tree.heading("name", text="Script Name")
        self.script_tree.heading("actions", text="Actions")
        self.script_tree.heading("modified", text="Modified")
        
        self.script_tree.column("name", width=250)
        self.script_tree.column("actions", width=100)
        self.script_tree.column("modified", width=150)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.script_tree.yview)
        self.script_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.script_tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll.grid(row=0, column=1, sticky="ns")
        
        # Fallback listbox (hidden by default)
        self.script_listbox = tk.Listbox(list_frame, height=12)
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(button_frame, text="Refresh", command=self._refresh_script_list).grid(
            row=0, column=1, padx=(0, 5)
        )
        ttk.Button(button_frame, text="Load", command=self._load_selected_script).grid(
            row=0, column=2, padx=(0, 5)
        )
        ttk.Button(button_frame, text="Delete", command=self._delete_selected_script).grid(
            row=0, column=3, padx=(0, 5)
        )
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).grid(
            row=0, column=4
        )
        
        # Bindings
        self.script_tree.bind("<Double-Button-1>", lambda e: self._load_selected_script())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
    
    def _refresh_script_list(self):
        """Refresh the script list."""
        # Clear existing items
        for item in self.script_tree.get_children():
            self.script_tree.delete(item)
        
        # Load saved sequences
        self.scripts = self.storage.list_saved_sequences()
        
        if not self.scripts:
            # Show message if no scripts
            self.script_tree.insert("", "end", values=("No saved scripts found", "", ""))
            return
        
        # Add scripts to tree
        for script in self.scripts:
            name = script.get('name', 'Unknown')
            action_count = script.get('action_count', 0)
            modified = script.get('modified', 'Unknown')
            
            self.script_tree.insert("", "end", values=(name, f"{action_count} actions", modified))
    
    def _load_selected_script(self):
        """Load the selected script."""
        selection = self.script_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a script to load.")
            return
        
        # Get selected index
        item = selection[0]
        index = self.script_tree.index(item)
        
        if index >= len(self.scripts):
            return
        
        script_info = self.scripts[index]
        filename = script_info.get('filename')
        
        if not filename:
            messagebox.showerror("Error", "Invalid script selection.")
            return
        
        # Load the sequence
        sequence = self.storage.load_sequence(filename)
        
        if sequence:
            if self.callback:
                self.callback(sequence)
            self.dialog.destroy()
        else:
            messagebox.showerror("Load Error", f"Failed to load script '{filename}'.")
    
    def _delete_selected_script(self):
        """Delete the selected script."""
        selection = self.script_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a script to delete.")
            return
        
        # Get selected index
        item = selection[0]
        index = self.script_tree.index(item)
        
        if index >= len(self.scripts):
            return
        
        script_info = self.scripts[index]
        filename = script_info.get('filename')
        name = script_info.get('name', filename)
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
            success = self.storage.delete_sequence(filename)
            
            if success:
                messagebox.showinfo("Deleted", f"Script '{name}' deleted successfully.")
                self._refresh_script_list()
            else:
                messagebox.showerror("Delete Error", f"Failed to delete script '{name}'.")
