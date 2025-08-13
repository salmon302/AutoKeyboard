# AutoKeyboard Presser

A Python-based auto keyboard presser and recorder application with hotkey support.

## Features

- Auto key pressing with configurable timing
- Record and store unlimited key sequences  
- Setup timing between each key press
- Setup repeat counts or continuous repeat
- Global hotkey support
- Persistent settings and recorded actions

## Requirements

- Python 3.7+
- Windows OS (for global hotkey support)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Usage

1. **Recording Keys**: Set a Start/Stop hotkey and press it to begin recording key presses
2. **Playing Back**: Set a Play hotkey to replay recorded sequences
3. **Timing Control**: Adjust time between presses (milliseconds)
4. **Repeat Options**: Set number of repetitions or enable continuous repeat
5. **Clear Actions**: Use Clear button to remove all recorded actions

## Project Structure

- `main.py` - Application entry point
- `src/gui/` - User interface components
- `src/core/` - Key recording and playback logic
- `src/data/` - Data models and storage
- `src/utils/` - Utility functions
