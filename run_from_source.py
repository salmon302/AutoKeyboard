"""
AutoKeyboard Presser - Python Source Launcher
This script runs the application directly from Python source without needing the compiled .exe
Recommended for users experiencing antivirus false positives.
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_python():
    """Check if Python is available."""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        else:
            return False, f"Python {version.major}.{version.minor}.{version.micro} (requires 3.7+)"
    except:
        return False, "Python not found"

def check_pynput():
    """Check if pynput is installed."""
    try:
        import pynput
        # Get version safely - pynput doesn't always have __version__
        try:
            version = pynput.__version__
        except AttributeError:
            version = "installed"
        return True, f"pynput {version}"
    except ImportError:
        return False, "pynput not installed"

def install_pynput():
    """Install pynput using pip."""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "pynput"], 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def main():
    """Main launcher function."""
    print("AutoKeyboard Presser - Python Source Launcher")
    print("=" * 50)
    
    # Check Python version
    python_ok, python_info = check_python()
    print(f"Python: {python_info}")
    
    if not python_ok:
        print("ERROR: Python 3.7+ is required!")
        print("Please install Python from https://python.org")
        input("Press Enter to exit...")
        return 1
    
    # Check pynput
    pynput_ok, pynput_info = check_pynput()
    print(f"pynput: {pynput_info}")
    
    if not pynput_ok:
        print("\nInstalling pynput...")
        install_ok, install_msg = install_pynput()
        if install_ok:
            print("✓ pynput installed successfully!")
        else:
            print(f"✗ Failed to install pynput: {install_msg}")
            input("Press Enter to exit...")
            return 1
    
    # Add src to path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    print("\n" + "=" * 50)
    print("Starting AutoKeyboard Presser...")
    print("=" * 50)
    
    try:
        # Import and run the main application
        from gui.main_window import MainWindow
        from core.key_recorder import KeyRecorder
        from core.key_player import KeyPlayer
        from core.hotkey_manager import HotkeyManager
        from data.settings import Settings
        
        # Create main application
        root = tk.Tk()
        settings = Settings()
        
        # Initialize core components
        key_recorder = KeyRecorder()
        key_player = KeyPlayer()
        hotkey_manager = HotkeyManager()
        
        # Initialize GUI
        main_window = MainWindow(
            root,
            key_recorder,
            key_player,
            hotkey_manager,
            settings
        )
        
        # Load saved settings
        settings.load()
        main_window.apply_settings(settings)
        
        # Set up window properties
        root.title("AutoKeyboard Presser v1.0 (Python Source)")
        root.geometry("500x400")
        root.resizable(False, False)
        
        # Handle window closing
        def on_closing():
            try:
                settings.save()
                key_recorder.stop_recording()
                key_player.stop_playback()
                hotkey_manager.cleanup()
                root.destroy()
            except Exception as e:
                print(f"Error during shutdown: {e}")
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the GUI
        print("✓ Application started successfully!")
        print("Close the application window to exit.")
        root.mainloop()
        
        return 0
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure all source files are present in the 'src' directory.")
        input("Press Enter to exit...")
        return 1
    except Exception as e:
        print(f"✗ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
