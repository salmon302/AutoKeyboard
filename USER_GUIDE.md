# AutoKeyboard Presser - User Guide

## Quick Start

1. **First Time Setup**:
   - Double-click `setup.bat` to install dependencies
   - Or run: `pip install -r requirements.txt`

2. **Running the Application**:
   - Double-click `run.bat` 
   - Or run: `python main.py`

## How to Use

### 1. Setting Up Hotkeys
- **Start/Stop Hotkey**: Choose from dropdown (default: F1)
  - Press once to start recording
  - Press again to stop recording
- **Play Hotkey**: Choose from dropdown (default: F2)
  - Press to play back recorded keys

### 2. Recording Keys
1. Set your Start/Stop hotkey
2. Press the hotkey to begin recording
3. Type the keys you want to record
4. Press the hotkey again to stop recording
5. Your recorded keys will appear in the action list

### 3. Playing Back Keys
1. Make sure you have recorded some keys
2. Set the timing between key presses (milliseconds)
3. Choose repeat mode:
   - **Repeat X times**: Play sequence a specific number of times
   - **Repeat continuously**: Play until you stop it
4. Press your Play hotkey to start playback

### 4. Timing Controls
- **Time between presses**: Delay between each key (1-10000 ms)
- **Repeat count**: How many times to repeat the sequence
- **Repeat continuously**: Loop the sequence indefinitely
- **Disable countdown timer**: Skip countdown before playback

### 5. Script Editing Features
- **Edit Script**: Open advanced script editor for manual editing
- **Save Script**: Save current recorded sequence to file
- **Load Script**: Load previously saved scripts
- **Script Templates**: Use built-in templates (Hello World, Copy/Paste, etc.)
- **Advanced Actions**: Add delays, key combinations, and complex sequences

#### Script Editor Features:
- **Manual Key Entry**: Add individual keys or combinations
- **Delay Controls**: Insert precise timing delays
- **Validation**: Check script syntax before applying
- **Templates**: Quick-start with common automation patterns
- **Export/Import**: Save scripts as human-readable files

#### Script Format:
```
KEY: a                # Press single key
KEY: ctrl+c           # Key combination  
DELAY: 1000          # Wait 1 second
KEY: Enter           # Special keys
```

### 6. Other Features
- **Clear**: Remove all recorded actions
- **Script Management**: Save, load, and organize automation scripts

## Hotkey Options

Available hotkeys include:
- Function keys: F1-F12
- Modified function keys: Ctrl+F1, Alt+F1, Shift+F1, etc.
- Choose "None" to disable a hotkey

## Tips

1. **Global Hotkeys**: Hotkeys work even when the application is minimized
2. **Safe Recording**: The app won't record its own hotkeys
3. **Timing**: Use longer delays for applications that need time to process
4. **Repeat**: Use continuous repeat for ongoing automation tasks

## Troubleshooting

**Hotkeys not working?**
- Try different hotkey combinations
- Make sure another application isn't using the same hotkey
- Run as administrator if needed

**Keys not recording?**
- Check that recording has started (status shows "Recording...")
- Some special keys may not be recordable

**Playback issues?**
- Increase timing between presses
- Make sure target application can accept input

## Technical Notes

- Built with Python 3.7+ and tkinter
- Uses pynput library for key handling
- Settings are automatically saved to `~/.autokeyboard/settings.json`
- Requires Windows for global hotkey support

## Limitations

- Windows only (for global hotkeys)
- Some protected applications may block key input
- Function keys may conflict with system hotkeys
