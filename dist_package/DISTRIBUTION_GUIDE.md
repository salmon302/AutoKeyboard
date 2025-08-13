# AutoKeyboard Presser - Distribution Guide

## Package Contents

This distribution package contains everything you need to run AutoKeyboard Presser:

### Executable Options
- **`AutoKeyboard-Presser.exe`** - Main executable (recommended for most users)
- **`run_from_source.py`** - Python source launcher (if antivirus issues occur)
- **`run_from_source.bat`** - Batch file to run Python source launcher

### Documentation
- **`README.md`** - Basic overview and quick start
- **`USER_GUIDE.md`** - Complete user guide with all features
- **`PORTABLE_README.md`** - Portable version information
- **`BUILD_INFO.md`** - Technical build information
- **`ANTIVIRUS_WARNING.md`** - Important antivirus information
- **`DISTRIBUTION_GUIDE.md`** - This file

### Utilities
- **`run.bat`** - Quick launcher for the executable

## Getting Started

### Option 1: Run Executable (Recommended)
1. Double-click `AutoKeyboard-Presser.exe`
2. If Windows Defender blocks it, see `ANTIVIRUS_WARNING.md`

### Option 2: Run from Python Source (If Antivirus Issues)
1. Ensure Python 3.8+ is installed
2. Double-click `run_from_source.bat`
3. The script will automatically install dependencies and run the app

## Security Notes

This software may trigger false positives in antivirus programs due to:
- Global hotkey monitoring
- Keyboard input simulation
- Executable packing (PyInstaller)

**This is normal for automation software.** See `ANTIVIRUS_WARNING.md` for details.

## System Requirements

- Windows 10/11
- Python 3.8+ (only if using source launcher)
- No additional dependencies for executable

## Features

- Global hotkey support (F1-F12)
- Key sequence recording and playback
- Script editor with templates
- Save/load custom scripts
- Configurable delays between actions
- Support for key combinations (Ctrl+C, Alt+Tab, etc.)

## Support

For issues or questions, refer to the documentation files or visit the project repository.

---
AutoKeyboard Presser v1.0
Built with Python, tkinter, and pynput
