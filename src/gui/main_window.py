"""
Main application window GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from core.key_recorder import KeyRecorder
from core.key_player import KeyPlayer
from core.hotkey_manager import HotkeyManager
from data.settings import Settings
from data.key_sequence import KeySequence
from data.action_storage import ActionStorage
from utils.key_utils import HOTKEY_OPTIONS, get_key_display_name
from gui.script_editor import ScriptEditorWindow, ScriptSaveDialog, ScriptLoadDialog


class MainWindow:
    """Main application window."""
    
    def __init__(self, root: tk.Tk, recorder: KeyRecorder, player: KeyPlayer, 
                 hotkey_manager: HotkeyManager, settings: Settings):
        self.root = root
        self.recorder = recorder
        self.player = player
        self.hotkey_manager = hotkey_manager
        self.settings = settings
        
        # Initialize action storage
        self.action_storage = ActionStorage()
        
        # State variables
        self.is_recording = False
        self.is_playing = False
        
        # Setup callbacks
        self._setup_callbacks()
        
        # Create GUI elements
        self._create_widgets()
        self._layout_widgets()
        self._setup_bindings()
        
    def _setup_callbacks(self):
        """Setup callbacks for core components."""
        # Recorder callbacks
        self.recorder.on_recording_started = self._on_recording_started
        self.recorder.on_recording_stopped = self._on_recording_stopped
        self.recorder.on_key_recorded = self._on_key_recorded
        
        # Player callbacks
        self.player.on_playback_started = self._on_playback_started
        self.player.on_playback_stopped = self._on_playback_stopped
        
        # Hotkey callbacks
        self.hotkey_manager.on_start_stop_pressed = self._on_start_stop_hotkey
        self.hotkey_manager.on_play_pressed = self._on_play_hotkey
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Hotkey section
        self.hotkey_frame = ttk.LabelFrame(self.main_frame, text="Hotkeys", padding="5")
        
        # Start/Stop hotkey
        self.start_stop_label = ttk.Label(self.hotkey_frame, text="Start/Stop Hotkey:")
        self.start_stop_var = tk.StringVar(value="F1")
        self.start_stop_combo = ttk.Combobox(
            self.hotkey_frame, 
            textvariable=self.start_stop_var,
            values=HOTKEY_OPTIONS,
            state="readonly",
            width=15
        )
        
        # Play hotkey
        self.play_label = ttk.Label(self.hotkey_frame, text="Play Hotkey:")
        self.play_var = tk.StringVar(value="F2")
        self.play_combo = ttk.Combobox(
            self.hotkey_frame,
            textvariable=self.play_var,
            values=HOTKEY_OPTIONS,
            state="readonly",
            width=15
        )
        
        # Action buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.clear_button = ttk.Button(self.button_frame, text="Clear", command=self._on_clear)
        self.edit_button = ttk.Button(self.button_frame, text="Edit Script", command=self._on_edit_script)
        self.save_button = ttk.Button(self.button_frame, text="Save Script", command=self._on_save_script)
        self.load_button = ttk.Button(self.button_frame, text="Load Script", command=self._on_load_script)
        
        # Action list
        self.action_frame = ttk.LabelFrame(self.main_frame, text="Recorded Actions", padding="5")
        
        # Create listbox with scrollbar
        self.list_frame = ttk.Frame(self.action_frame)
        self.action_listbox = tk.Listbox(
            self.list_frame,
            height=8,
            width=50,
            font=("Consolas", 9)
        )
        self.action_scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical")
        self.action_listbox.config(yscrollcommand=self.action_scrollbar.set)
        self.action_scrollbar.config(command=self.action_listbox.yview)
        
        # Timing controls
        self.timing_frame = ttk.LabelFrame(self.main_frame, text="Timing & Repeat", padding="5")
        
        # Time between presses
        self.timing_label = ttk.Label(self.timing_frame, text="Time between presses:")
        self.timing_var = tk.IntVar(value=500)
        self.timing_spinbox = ttk.Spinbox(
            self.timing_frame,
            from_=1,
            to=10000,
            textvariable=self.timing_var,
            width=10
        )
        self.timing_ms_label = ttk.Label(self.timing_frame, text="milliseconds")
        
        # Repeat controls
        self.repeat_frame = ttk.Frame(self.timing_frame)
        
        self.repeat_var = tk.IntVar(value=1)
        self.repeat_radio1 = ttk.Radiobutton(
            self.repeat_frame,
            text="Repeat",
            variable=self.repeat_var,
            value=1,
            command=self._on_repeat_mode_changed
        )
        
        self.repeat_count_var = tk.IntVar(value=1)
        self.repeat_count_spinbox = ttk.Spinbox(
            self.repeat_frame,
            from_=1,
            to=1000,
            textvariable=self.repeat_count_var,
            width=8
        )
        self.repeat_times_label = ttk.Label(self.repeat_frame, text="times")
        
        self.repeat_radio2 = ttk.Radiobutton(
            self.repeat_frame,
            text="Repeat continuously",
            variable=self.repeat_var,
            value=2,
            command=self._on_repeat_mode_changed
        )
        
        # Countdown timer
        self.countdown_var = tk.BooleanVar(value=False)
        self.countdown_check = ttk.Checkbutton(
            self.timing_frame,
            text="Disable countdown timer",
            variable=self.countdown_var
        )
        
        # Status and control
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_var = tk.StringVar(value="Status: No Keys Recorded Yet")
        self.status_label = ttk.Label(
            self.status_frame,
            textvariable=self.status_var,
            font=("Arial", 9, "bold")
        )
        
        self.exit_button = ttk.Button(
            self.status_frame,
            text="Exit",
            command=self._on_exit
        )
    
    def _layout_widgets(self):
        """Layout all widgets in the window."""
        
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Hotkey section
        self.hotkey_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.start_stop_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.start_stop_combo.grid(row=0, column=1, padx=(0, 20))
        
        self.play_label.grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.play_combo.grid(row=0, column=3)
        
        # Action buttons
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.clear_button.grid(row=0, column=0, padx=(0, 5))
        self.edit_button.grid(row=0, column=1, padx=(0, 5))
        self.save_button.grid(row=0, column=2, padx=(0, 5))
        self.load_button.grid(row=0, column=3)
        
        # Action list
        self.action_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        self.main_frame.rowconfigure(2, weight=1)
        
        self.list_frame.grid(row=0, column=0, sticky="nsew")
        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.rowconfigure(0, weight=1)
        
        self.action_listbox.grid(row=0, column=0, sticky="nsew")
        self.action_scrollbar.grid(row=0, column=1, sticky="ns")
        self.list_frame.columnconfigure(0, weight=1)
        self.list_frame.rowconfigure(0, weight=1)
        
        # Timing controls
        self.timing_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.timing_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.timing_spinbox.grid(row=0, column=1, padx=(0, 5))
        self.timing_ms_label.grid(row=0, column=2, sticky="w")
        
        self.repeat_frame.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))
        
        self.repeat_radio1.grid(row=0, column=0, sticky="w")
        self.repeat_count_spinbox.grid(row=0, column=1, padx=(5, 5))
        self.repeat_times_label.grid(row=0, column=2, sticky="w")
        
        self.repeat_radio2.grid(row=1, column=0, columnspan=3, sticky="w", pady=(2, 0))
        
        self.countdown_check.grid(row=2, column=0, columnspan=3, sticky="w", pady=(5, 0))
        
        # Status and exit
        self.status_frame.grid(row=4, column=0, columnspan=2, sticky="ew")
        self.status_frame.columnconfigure(0, weight=1)
        
        self.status_label.grid(row=0, column=0, sticky="w")
        self.exit_button.grid(row=0, column=1)
    
    def _setup_bindings(self):
        """Setup event bindings."""
        # Hotkey combo changes
        self.start_stop_combo.bind("<<ComboboxSelected>>", self._on_start_stop_hotkey_changed)
        self.play_combo.bind("<<ComboboxSelected>>", self._on_play_hotkey_changed)
        
        # Timing changes
        self.timing_spinbox.bind("<FocusOut>", self._on_timing_changed)
        self.timing_spinbox.bind("<Return>", self._on_timing_changed)
        
        self.repeat_count_spinbox.bind("<FocusOut>", self._on_repeat_count_changed)
        self.repeat_count_spinbox.bind("<Return>", self._on_repeat_count_changed)
    
    # Event handlers
    def _on_start_stop_hotkey_changed(self, event=None):
        """Handle start/stop hotkey selection change."""
        hotkey = self.start_stop_var.get()
        if self.hotkey_manager.set_start_stop_hotkey(hotkey):
            self.settings.set('start_stop_hotkey', hotkey)
    
    def _on_play_hotkey_changed(self, event=None):
        """Handle play hotkey selection change."""
        hotkey = self.play_var.get()
        if self.hotkey_manager.set_play_hotkey(hotkey):
            self.settings.set('play_hotkey', hotkey)
    
    def _on_timing_changed(self, event=None):
        """Handle timing value change."""
        timing = self.timing_var.get()
        self.player.set_timing(timing)
        self.settings.set('time_between_presses', timing)
    
    def _on_repeat_mode_changed(self):
        """Handle repeat mode change."""
        mode = self.repeat_var.get()
        if mode == 1:  # Specific count
            count = self.repeat_count_var.get()
            self.player.set_repeat_count(count)
            self.settings.set('repeat_continuously', False)
        else:  # Continuous
            self.player.set_repeat_continuously(True)
            self.settings.set('repeat_continuously', True)
    
    def _on_repeat_count_changed(self, event=None):
        """Handle repeat count change."""
        if self.repeat_var.get() == 1:
            count = self.repeat_count_var.get()
            self.player.set_repeat_count(count)
            self.settings.set('repeat_count', count)
    
    def _on_load_script(self):
        """Handle load script button."""
        # Show script selection dialog
        ScriptLoadDialog(self.root, self.action_storage, self._on_script_loaded)
    
    def _on_save_script(self):
        """Handle save script button."""
        sequence = self.recorder.get_recorded_sequence()
        if not sequence or not sequence.actions:
            messagebox.showwarning("No Script", "No actions recorded to save.")
            return
        
        # Show script save dialog
        ScriptSaveDialog(self.root, self.action_storage, sequence, self._on_script_save_completed)
    
    def _on_script_loaded(self, sequence: KeySequence):
        """Handle script loaded from file."""
        # Set the loaded sequence as current
        self.recorder.current_sequence = sequence
        
        # Update display
        self._update_action_list_from_sequence(sequence)
        
        # Update status
        key_count = len([a for a in sequence.actions if a.action_type.value == "key_press"])
        self.status_var.set(f"Status: Script loaded - {key_count} keys")
    
    def _on_script_save_completed(self, success: bool, filename: str):
        """Handle script save completion."""
        if success:
            messagebox.showinfo("Script Saved", f"Script saved successfully as '{filename}'")
        else:
            messagebox.showerror("Save Error", f"Failed to save script '{filename}'")
    
    def _update_action_list_from_sequence(self, sequence: KeySequence):
        """Update the action list display from a sequence."""
        self.action_listbox.delete(0, tk.END)
        
        for action in sequence.actions:
            if action.action_type.value == "key_press":
                try:
                    from utils.key_utils import parse_key_code
                    key = parse_key_code(action.key)
                    key_name = get_key_display_name(key) if key else action.key
                except:
                    key_name = str(action.key)
                self.action_listbox.insert(tk.END, f"Key: {key_name}")
            elif action.action_type.value == "delay":
                delay_ms = int(action.duration * 1000) if action.duration else 0
                self.action_listbox.insert(tk.END, f"Delay: {delay_ms}ms")

    def _on_clear(self):
        """Handle clear button."""
        self.recorder.clear_sequence()
        self.action_listbox.delete(0, tk.END)
        self.status_var.set("Status: No Keys Recorded Yet")
    
    def _on_script_saved(self, new_sequence: KeySequence):
        """Handle script editor save."""
        # Replace the current sequence with the edited one
        self.recorder.current_sequence = new_sequence
        
        # Update the action list display
        self.action_listbox.delete(0, tk.END)
        
        # Add actions to display
        key_count = 0
        for action in new_sequence.actions:
            if action.action_type.value == "key_press":
                try:
                    from utils.key_utils import parse_key_code
                    key = parse_key_code(action.key)
                    key_name = get_key_display_name(key) if key else action.key
                except:
                    key_name = str(action.key)
                self.action_listbox.insert(tk.END, f"Key: {key_name}")
                key_count += 1
            elif action.action_type.value == "delay":
                delay_ms = int(action.duration * 1000) if action.duration else 0
                self.action_listbox.insert(tk.END, f"Delay: {delay_ms}ms")
        
        # Update status
        if key_count > 0:
            self.status_var.set(f"Status: {key_count} keys loaded from script")
        else:
            self.status_var.set("Status: Script loaded (no keys)")
    
    def _on_edit_script(self):
        """Handle edit script button."""
        sequence = self.recorder.get_recorded_sequence()
        if not sequence or not sequence.actions:
            # Create empty sequence for editing
            sequence = KeySequence("New Script")
        
        # Open script editor
        editor = ScriptEditorWindow(
            self.root,
            sequence,
            self._on_script_saved
        )
    
    def _on_exit(self):
        """Handle exit button."""
        self.root.quit()
    
    # Callback handlers for core components
    def _on_recording_started(self):
        """Handle recording started."""
        self.is_recording = True
        self.status_var.set("Status: Recording... Press Start/Stop hotkey to stop")
        self.clear_button.config(state="disabled")
    
    def _on_recording_stopped(self):
        """Handle recording stopped."""
        self.is_recording = False
        sequence = self.recorder.get_recorded_sequence()
        count = sequence.get_key_count()
        self.status_var.set(f"Status: {count} keys recorded")
        self.clear_button.config(state="normal")
    
    def _on_key_recorded(self, action):
        """Handle key recorded."""
        # Add key to listbox
        try:
            from utils.key_utils import parse_key_code
            key = parse_key_code(action.key)
            key_name = get_key_display_name(key) if key else action.key
        except:
            key_name = str(action.key)
        self.action_listbox.insert(tk.END, f"Key: {key_name}")
        self.action_listbox.see(tk.END)
    
    def _on_playback_started(self):
        """Handle playback started."""
        self.is_playing = True
        self.status_var.set("Status: Playing back recorded keys...")
        self.clear_button.config(state="disabled")
    
    def _on_playback_stopped(self):
        """Handle playback stopped."""
        self.is_playing = False
        sequence = self.recorder.get_recorded_sequence()
        count = sequence.get_key_count()
        self.status_var.set(f"Status: {count} keys recorded")
        self.clear_button.config(state="normal")
    
    def _on_start_stop_hotkey(self):
        """Handle start/stop hotkey pressed."""
        if self.is_recording:
            self.recorder.stop_recording()
        elif not self.is_playing:
            self.recorder.start_recording()
    
    def _on_play_hotkey(self):
        """Handle play hotkey pressed."""
        if not self.is_recording and not self.is_playing:
            sequence = self.recorder.get_recorded_sequence()
            if sequence:
                self.player.start_playback(sequence)
            else:
                # Can't show messagebox from hotkey thread, update status instead
                self.status_var.set("Status: No keys recorded to play")
    
    def apply_settings(self, settings: Settings):
        """Apply saved settings to the GUI."""
        # Hotkeys
        self.start_stop_var.set(settings.get('start_stop_hotkey', 'F1'))
        self.play_var.set(settings.get('play_hotkey', 'F2'))
        
        # Timing
        timing = settings.get('time_between_presses', 500)
        self.timing_var.set(timing)
        self.player.set_timing(timing)
        
        # Repeat
        repeat_count = settings.get('repeat_count', 1)
        repeat_continuously = settings.get('repeat_continuously', False)
        
        self.repeat_count_var.set(repeat_count)
        if repeat_continuously:
            self.repeat_var.set(2)
            self.player.set_repeat_continuously(True)
        else:
            self.repeat_var.set(1)
            self.player.set_repeat_count(repeat_count)
        
        # Countdown
        self.countdown_var.set(settings.get('disable_countdown_timer', False))
        
        # Apply hotkeys
        self.hotkey_manager.set_start_stop_hotkey(self.start_stop_var.get())
        self.hotkey_manager.set_play_hotkey(self.play_var.get())
        self.hotkey_manager.start()
