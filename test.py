#!/usr/bin/env python3
"""
Test script for AutoKeyboard Presser
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Testing imports...")

try:
    print("Importing tkinter...")
    import tkinter as tk
    print("✓ tkinter imported successfully")
    
    print("Importing pynput...")
    import pynput
    print("✓ pynput imported successfully")
    
    print("Importing data models...")
    from data.settings import Settings
    from data.key_sequence import KeySequence
    print("✓ data models imported successfully")
    
    print("Importing core components...")
    from core.key_recorder import KeyRecorder
    from core.key_player import KeyPlayer
    from core.hotkey_manager import HotkeyManager
    print("✓ core components imported successfully")
    
    print("Importing GUI...")
    from gui.main_window import MainWindow
    print("✓ GUI imported successfully")
    
    print("\nAll imports successful! Creating test window...")
    
    # Create a minimal test window
    root = tk.Tk()
    root.title("AutoKeyboard Test")
    root.geometry("300x200")
    
    label = tk.Label(root, text="AutoKeyboard Presser\nTest Window", font=("Arial", 12))
    label.pack(expand=True)
    
    button = tk.Button(root, text="Close", command=root.quit)
    button.pack(pady=10)
    
    print("Test window created. Close the window to continue...")
    root.mainloop()
    
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    
input("Press Enter to exit...")
