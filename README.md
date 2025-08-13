# AutoKeyboard Presser

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A powerful and user-friendly keyboard automation tool for Windows that allows you to record, edit, and replay key sequences with precision timing control and global hotkey support.

## 🚀 Features

### Core Functionality
- **🎥 Key Recording**: Record unlimited key sequences with precise timing
- **⏯️ Smart Playback**: Replay sequences with configurable timing and repeat options
- **⌨️ Global Hotkeys**: Control recording and playback from anywhere with customizable hotkeys
- **📝 Script Editor**: Advanced script editing with templates and manual key entry
- **💾 Persistent Storage**: Automatically save and load your automation scripts

### Advanced Features
- **⚡ Quick Setup Mode**: Create simple automations in seconds
- **🔄 Flexible Repeat Options**: Set exact repetition counts or continuous loops
- **⏱️ Precise Timing Control**: Adjust delays between keystrokes (1-10000ms)
- **📋 Script Templates**: Built-in templates for common automation tasks
- **🛡️ Safe Operation**: Smart filtering to prevent recording hotkeys

## 🔧 Requirements

- **Operating System**: Windows 10/11 (global hotkeys require Windows)
- **Python**: 3.7 or higher
- **Dependencies**: See `requirements.txt`

## 📦 Installation

### Option 1: Download Pre-built Executable (Recommended)
1. Download the latest `AutoKeyboard-Presser.exe` from the [Releases](../../releases) page
2. Run the executable directly - no installation required!
3. **Note**: Windows Defender may show a warning (this is a false positive due to unsigned executable)

### Option 2: Run from Source
1. Clone this repository:
   ```bash
   git clone https://github.com/salmon302/AutoKeyboard.git
   cd AutoKeyboard
   ```

2. Set up the environment:
   ```bash
   # Windows
   .\setup.bat
   
   # Or manually:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   # Or use: .\run.bat
   ```

## 🎯 Quick Start Guide

### 1. Basic Recording
1. **Set Hotkeys**: Configure your Start/Stop and Play hotkeys (default: F1/F2)
2. **Start Recording**: Press your Start/Stop hotkey (F1)
3. **Type Keys**: Perform the actions you want to automate
4. **Stop Recording**: Press Start/Stop hotkey again (F1)
5. **Playback**: Press your Play hotkey (F2) to replay the sequence

### 2. Quick Setup Mode
For simple automations:
1. Click **"Quick Setup"**
2. **"Capture Key"** - Press the key you want to automate
3. **Set Timing** - Configure delay between presses
4. **Choose Repeat Mode** - Set count or continuous
5. **"Create Automation"** - Ready to use!

### 3. Advanced Script Editing
- Use **"Edit Script"** for manual sequence creation
- Add delays, key combinations, and complex patterns
- Save and load automation scripts
- Use built-in templates for common tasks

## 📋 Usage Examples

### Text Automation
```
KEY: Hello World!
DELAY: 1000
KEY: Enter
```

### Copy-Paste Workflow
```
KEY: ctrl+c
DELAY: 500
KEY: ctrl+v
KEY: Enter
```

### Gaming Macros
```
KEY: w
DELAY: 100
KEY: a
DELAY: 100
KEY: s
DELAY: 100
KEY: d
```

## ⚠️ Security Notice

**This tool creates keyboard input which may trigger antivirus warnings.**

- **✅ Safe**: Open source, no network activity, local data only
- **🔍 Verified**: All source code is available for inspection
- **🛡️ Privacy**: No data collection or transmission
- **📝 Transparent**: Built from verified Python source

If your antivirus flags the executable, you can:
1. Add to antivirus whitelist/exclusions
2. Run from Python source (most secure)
3. Check file on VirusTotal.com
4. Review source code yourself

## 🏗️ Project Structure

```
AutoKeyboard/
├── main.py                 # Application entry point
├── src/
│   ├── core/              # Core automation logic
│   │   ├── key_recorder.py    # Key recording functionality
│   │   ├── key_player.py      # Key playback engine
│   │   └── hotkey_manager.py  # Global hotkey handling
│   ├── gui/               # User interface
│   │   ├── main_window.py     # Main application window
│   │   ├── script_editor.py   # Script editing interface
│   │   └── key_capture_dialog.py # Hotkey capture dialogs
│   ├── data/              # Data management
│   │   ├── settings.py        # Configuration management
│   │   ├── key_sequence.py    # Key sequence data models
│   │   └── action_storage.py  # Script storage system
│   └── utils/             # Utility functions
│       └── key_utils.py       # Key handling utilities
├── requirements.txt       # Python dependencies
├── setup.bat             # Environment setup script
├── build.bat             # Build executable script
└── docs/                 # Documentation
    ├── USER_GUIDE.md     # Detailed user guide
    └── ANTIVIRUS_WARNING.md # Security information
```

## 🔧 Building from Source

To create your own executable:

```bash
# Setup environment
.\setup.bat

# Build executable
.\build.bat

# The AutoKeyboard-Presser.exe will be created
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Coding standards
- Pull request process
- Issue reporting guidelines

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **📖 Documentation**: Check [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions
- **🐛 Issues**: Report bugs on the [Issues](../../issues) page
- **💡 Feature Requests**: Suggest improvements via Issues
- **🔒 Security**: Review [ANTIVIRUS_WARNING.md](ANTIVIRUS_WARNING.md) for security info

## ⚖️ Disclaimer

This software is for legitimate automation purposes only. Users are responsible for complying with applicable laws and terms of service when using automation tools. The developers are not responsible for misuse of this software.

---

**Made with ❤️ for productivity and automation enthusiasts!**
