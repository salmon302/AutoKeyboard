# Contributing to AutoKeyboard

Thank you for your interest in contributing to AutoKeyboard! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git
- Windows 10/11 (for testing global hotkey functionality)
- Code editor (VS Code recommended)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/AutoKeyboard.git
   cd AutoKeyboard
   ```

2. **Set up Virtual Environment**
   ```bash
   # Windows
   .\setup.bat
   
   # Or manually:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -r requirements-dev.txt  # If exists
   # Or manually install testing tools:
   pip install pytest pytest-cov black flake8 mypy
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

## 📋 Development Guidelines

### Code Style

**Python Code Style:**
- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting: `black .`
- Use [flake8](https://flake8.pycqa.org/) for linting: `flake8 src/`
- Maximum line length: 88 characters (Black default)

**Naming Conventions:**
- Classes: `PascalCase` (e.g., `KeyRecorder`)
- Functions/Methods: `snake_case` (e.g., `start_recording`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_SEQUENCE_LENGTH`)
- Private methods: `_snake_case` (e.g., `_setup_callbacks`)

**Documentation:**
- All public classes and methods must have docstrings
- Use Google-style docstrings
- Include type hints for all function parameters and return values

**Example:**
```python
def record_key_sequence(self, duration: float) -> KeySequence:
    """Record a sequence of key presses for the specified duration.
    
    Args:
        duration: Recording duration in seconds.
        
    Returns:
        The recorded key sequence.
        
    Raises:
        RecordingError: If recording fails to start.
    """
```

### Project Structure

```
AutoKeyboard/
├── src/                   # Source code
│   ├── core/             # Core automation logic
│   ├── gui/              # User interface components
│   ├── data/             # Data models and storage
│   └── utils/            # Utility functions
├── tests/                # Unit tests
├── docs/                 # Documentation
├── scripts/              # Build and utility scripts
└── examples/             # Example automation scripts
```

### Git Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clean, documented code
   - Add/update tests as needed
   - Update documentation

3. **Test Your Changes**
   ```bash
   # Run tests
   python -m pytest
   
   # Check code style
   black --check .
   flake8 src/
   
   # Type checking
   mypy src/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(recorder): add pause/resume functionality
fix(gui): resolve hotkey capture dialog crash
docs: update installation instructions
test(core): add unit tests for key player
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_key_recorder.py

# Run with verbose output
python -m pytest -v
```

### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names: `test_should_record_key_sequence_when_recording_started`
- Test both success and failure cases
- Mock external dependencies (file system, GUI, etc.)

**Example Test:**
```python
import pytest
from unittest.mock import Mock, patch
from src.core.key_recorder import KeyRecorder


class TestKeyRecorder:
    def test_should_start_recording_successfully(self):
        # Arrange
        recorder = KeyRecorder()
        
        # Act
        result = recorder.start_recording()
        
        # Assert
        assert result is True
        assert recorder.is_recording is True
        
    def test_should_not_start_recording_when_already_recording(self):
        # Arrange
        recorder = KeyRecorder()
        recorder.start_recording()
        
        # Act
        result = recorder.start_recording()
        
        # Assert
        assert result is False
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Operating System and version
   - Python version
   - AutoKeyboard version

2. **Bug Description**
   - Clear description of the issue
   - Expected vs actual behavior
   - Steps to reproduce

3. **Additional Information**
   - Error messages/stack traces
   - Screenshots (if applicable)
   - Relevant configuration/settings

**Bug Report Template:**
```markdown
## Bug Description
Brief description of the bug.

## Environment
- OS: Windows 11
- Python: 3.9.7
- AutoKeyboard: v1.1.0

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Additional Information
Any other relevant information.
```

## 💡 Feature Requests

When requesting features:

1. **Describe the Feature**
   - Clear description of the requested functionality
   - Use case and benefits
   - Proposed implementation (if you have ideas)

2. **Consider Scope**
   - Should it be a core feature or plugin?
   - Impact on existing functionality
   - Complexity and maintenance implications

## 🔒 Security Considerations

Since AutoKeyboard handles keyboard input:

1. **Be Security Conscious**
   - Never log sensitive keystrokes
   - Ensure safe handling of user data
   - Consider privacy implications

2. **Report Security Issues**
   - Email security issues privately (don't create public issues)
   - Provide detailed information
   - Allow time for fixes before disclosure

## 📖 Documentation

### Code Documentation
- Document all public APIs
- Include usage examples
- Keep docstrings up to date

### User Documentation
- Update `USER_GUIDE.md` for user-facing features
- Update `README.md` for installation/setup changes
- Add examples for new features

## 🎯 Areas for Contribution

**Good First Issues:**
- Documentation improvements
- Bug fixes
- Unit test additions
- Code style improvements

**Advanced Features:**
- Cross-platform support
- Plugin system
- Advanced script editing
- Performance optimizations

**Infrastructure:**
- CI/CD setup
- Automated testing
- Release automation
- Package distribution

## 💬 Communication

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for general questions
- **Code Review**: All changes require review via Pull Requests

## 📜 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and contribute
- Follow the project's best interests
