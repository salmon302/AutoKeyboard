#!/usr/bin/env python3
"""
AutoKeyboard Presser - Main Application Entry Point

A keyboard automation tool for recording and playing back key sequences
with configurable timing and hotkey support.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Handle PyInstaller frozen executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = os.path.dirname(sys.executable)
    src_path = os.path.join(application_path, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

from gui.main_window import MainWindow
from core.key_recorder import KeyRecorder
from core.key_player import KeyPlayer
from core.hotkey_manager import HotkeyManager
from data.settings import Settings


class AutoKeyboardApp:
    """Main application controller."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.settings = Settings()
        
        # Initialize core components
        self.key_recorder = KeyRecorder()
        self.key_player = KeyPlayer()
        self.hotkey_manager = HotkeyManager()
        
        # Initialize GUI
        self.main_window = MainWindow(
            self.root,
            self.key_recorder,
            self.key_player,
            self.hotkey_manager,
            self.settings
        )
        
        # Load saved settings
        self.settings.load()
        self.main_window.apply_settings(self.settings)
        
    def run(self):
        """Start the application main loop."""
        try:
            # Set up window properties
            self.root.title("AutoKeyboard Presser v1.1")
            self.root.geometry("650x450")
            self.root.resizable(False, False)
            
            # Handle window closing
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Start the GUI
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Application error: {str(e)}")
            
    def on_closing(self):
        """Handle application shutdown."""
        try:
            # Save settings
            self.settings.save()
            
            # Stop any running operations
            self.key_recorder.stop_recording()
            self.key_player.stop_playback()
            self.hotkey_manager.cleanup()
            
            # Close application
            self.root.destroy()
            
        except Exception as e:
            print(f"Error during shutdown: {e}")
            self.root.destroy()


def main():
    """Application entry point."""
    try:
        app = AutoKeyboardApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
