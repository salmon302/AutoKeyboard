"""
Key capture dialog for defining hotkeys and single keys.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Set
from pynput import keyboard
import threading
import time


class KeyCaptureDialog:
    """Dialog for capturing key presses to define hotkeys."""
    
    def __init__(self, parent: tk.Tk, title: str = "Capture Key", 
                 callback: Optional[Callable[[str], None]] = None,
                 allow_combinations: bool = True):
        self.parent = parent
        self.callback = callback
        self.allow_combinations = allow_combinations
        
        # State
        self.captured_keys: Set[str] = set()
        self.current_combination = ""
        self.listener: Optional[keyboard.Listener] = None
        self.is_capturing = False
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self._create_widgets()
        self._start_capture()
        
        # Handle dialog close
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def _create_widgets(self):
        """Create dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Instructions
        instruction_text = "Press any key or key combination"
        if not self.allow_combinations:
            instruction_text = "Press any single key"
            
        self.instruction_label = ttk.Label(
            main_frame,
            text=instruction_text,
            font=("Arial", 12, "bold")
        )
        self.instruction_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Captured Key", padding="10")
        status_frame.pack(fill="x", pady=(0, 20))
        
        self.status_var = tk.StringVar(value="Waiting for key press...")
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Consolas", 11),
            foreground="blue"
        )
        self.status_label.pack()
        
        # Help text
        help_frame = ttk.LabelFrame(main_frame, text="Help", padding="10")
        help_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        help_text = "• Press any key to capture it\n"
        if self.allow_combinations:
            help_text += "• Hold modifiers (Ctrl, Alt, Shift) and press another key for combinations\n"
        help_text += "• Click 'Use This Key' to confirm\n• Click 'Cancel' to abort"
        
        help_label = ttk.Label(
            help_frame,
            text=help_text,
            justify="left",
            font=("Arial", 9)
        )
        help_label.pack(anchor="w")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        self.cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel
        )
        self.cancel_button.pack(side="right")
        
        self.use_button = ttk.Button(
            button_frame,
            text="Use This Key",
            command=self._on_use_key,
            state="disabled"
        )
        self.use_button.pack(side="right", padx=(0, 10))
        
    def _start_capture(self):
        """Start key capture."""
        self.is_capturing = True
        
        def on_key_event(key, is_press):
            """Handle key press/release events."""
            if not self.is_capturing:
                return
                
            try:
                # Get key name
                if hasattr(key, 'char') and key.char:
                    key_name = key.char.upper()
                else:
                    key_name = str(key).replace('Key.', '').replace('_', ' ').title()
                
                if is_press:
                    self.captured_keys.add(key_name)
                else:
                    self.captured_keys.discard(key_name)
                
                # Update combination
                self._update_combination()
                
            except Exception as e:
                print(f"Error in key capture: {e}")
        
        def on_press(key):
            """Handle key press."""
            on_key_event(key, True)
        
        def on_release(key):
            """Handle key release."""
            on_key_event(key, False)
            
            # For single key mode, capture immediately on release
            if not self.allow_combinations and self.current_combination:
                self.dialog.after(100, self._auto_accept)  # Small delay to show the key
        
        # Start listener in separate thread
        self.listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )
        self.listener.start()
        
    def _update_combination(self):
        """Update the current key combination display."""
        if not self.captured_keys:
            combination = "Waiting for key press..."
            self.use_button.config(state="disabled")
        else:
            # Sort keys: modifiers first, then others
            modifiers = []
            regular_keys = []
            
            for key in self.captured_keys:
                if key.lower() in ['ctrl', 'alt', 'shift', 'cmd', 'control', 'menu', 'windows']:
                    modifiers.append(key)
                else:
                    regular_keys.append(key)
            
            # Build combination string
            all_keys = sorted(modifiers) + sorted(regular_keys)
            combination = "+".join(all_keys)
            
            self.use_button.config(state="normal")
        
        self.current_combination = combination
        self.status_var.set(combination)
        
    def _auto_accept(self):
        """Auto-accept for single key mode."""
        if self.current_combination and self.current_combination != "Waiting for key press...":
            self._on_use_key()
    
    def _on_use_key(self):
        """Handle use key button."""
        if self.current_combination and self.current_combination != "Waiting for key press...":
            self._stop_capture()
            if self.callback:
                self.callback(self.current_combination)
            self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle cancel button."""
        self._stop_capture()
        self.dialog.destroy()
    
    def _on_close(self):
        """Handle dialog close."""
        self._stop_capture()
        self.dialog.destroy()
    
    def _stop_capture(self):
        """Stop key capture."""
        self.is_capturing = False
        if self.listener:
            try:
                self.listener.stop()
            except:
                pass
            self.listener = None


class QuickSetupDialog:
    """Dialog for quick setup of single key automation."""
    
    def __init__(self, parent: tk.Tk, callback: Optional[Callable[[str, int, int, bool], None]] = None):
        self.parent = parent
        self.callback = callback
        self.selected_key = ""
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Quick Setup - Single Key Automation")
        self.dialog.geometry("450x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self._create_widgets()
        
        # Handle dialog close
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def _create_widgets(self):
        """Create dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Quick Setup - Single Key Automation",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Key selection
        key_frame = ttk.LabelFrame(main_frame, text="1. Select Key to Automate", padding="10")
        key_frame.pack(fill="x", pady=(0, 15))
        
        key_inner_frame = ttk.Frame(key_frame)
        key_inner_frame.pack(fill="x")
        
        self.key_var = tk.StringVar(value="No key selected")
        self.key_label = ttk.Label(
            key_inner_frame,
            textvariable=self.key_var,
            font=("Consolas", 11),
            foreground="blue"
        )
        self.key_label.pack(side="left")
        
        self.select_key_button = ttk.Button(
            key_inner_frame,
            text="Capture Key",
            command=self._on_capture_key
        )
        self.select_key_button.pack(side="right")
        
        # Timing controls
        timing_frame = ttk.LabelFrame(main_frame, text="2. Configure Timing", padding="10")
        timing_frame.pack(fill="x", pady=(0, 15))
        
        # Delay between presses
        delay_frame = ttk.Frame(timing_frame)
        delay_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(delay_frame, text="Delay between presses:").pack(side="left")
        
        self.delay_var = tk.IntVar(value=1000)
        self.delay_spinbox = ttk.Spinbox(
            delay_frame,
            from_=100,
            to=10000,
            textvariable=self.delay_var,
            width=8
        )
        self.delay_spinbox.pack(side="right", padx=(5, 0))
        
        ttk.Label(delay_frame, text="milliseconds").pack(side="right")
        
        # Repeat options
        repeat_frame = ttk.LabelFrame(main_frame, text="3. Configure Repeat", padding="10")
        repeat_frame.pack(fill="x", pady=(0, 20))
        
        self.repeat_var = tk.IntVar(value=1)
        
        # Specific count
        count_frame = ttk.Frame(repeat_frame)
        count_frame.pack(fill="x", pady=(0, 5))
        
        self.count_radio = ttk.Radiobutton(
            count_frame,
            text="Repeat",
            variable=self.repeat_var,
            value=1
        )
        self.count_radio.pack(side="left")
        
        self.count_var = tk.IntVar(value=10)
        self.count_spinbox = ttk.Spinbox(
            count_frame,
            from_=1,
            to=1000,
            textvariable=self.count_var,
            width=8
        )
        self.count_spinbox.pack(side="left", padx=(5, 5))
        
        ttk.Label(count_frame, text="times").pack(side="left")
        
        # Continuous
        self.continuous_radio = ttk.Radiobutton(
            repeat_frame,
            text="Repeat continuously (until stopped)",
            variable=self.repeat_var,
            value=2
        )
        self.continuous_radio.pack(anchor="w", pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        self.cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_close
        )
        self.cancel_button.pack(side="right")
        
        self.create_button = ttk.Button(
            button_frame,
            text="Create Automation",
            command=self._on_create,
            state="disabled"
        )
        self.create_button.pack(side="right", padx=(0, 10))
        
    def _on_capture_key(self):
        """Handle capture key button."""
        def on_key_captured(key_combination):
            self.selected_key = key_combination
            self.key_var.set(f"Selected: {key_combination}")
            self.create_button.config(state="normal")
        
        KeyCaptureDialog(
            self.dialog,
            "Capture Key for Automation",
            on_key_captured,
            allow_combinations=False  # Single key only
        )
    
    def _on_create(self):
        """Handle create automation button."""
        if not self.selected_key:
            return
            
        delay = self.delay_var.get()
        repeat_mode = self.repeat_var.get()
        
        if repeat_mode == 1:
            # Specific count
            repeat_count = self.count_var.get()
            continuous = False
        else:
            # Continuous
            repeat_count = 0
            continuous = True
        
        if self.callback:
            self.callback(self.selected_key, delay, repeat_count, continuous)
        
        self.dialog.destroy()
    
    def _on_close(self):
        """Handle dialog close."""
        self.dialog.destroy()
