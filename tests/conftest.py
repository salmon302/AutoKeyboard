# Test configuration and fixtures for AutoKeyboard

import pytest
import sys
import os

# Add src directory to path for imports during testing
src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)


@pytest.fixture
def mock_settings():
    """Fixture providing a mock settings object."""
    from data.settings import Settings
    settings = Settings()
    # Don't save/load during tests
    settings.save = lambda: None
    settings.load = lambda: None
    return settings


@pytest.fixture
def mock_key_sequence():
    """Fixture providing a mock key sequence."""
    from data.key_sequence import KeySequence, KeyAction, ActionType
    sequence = KeySequence()
    
    # Add some sample actions
    sequence.add_action(KeyAction(ActionType.KEY_PRESS, "a", 0.0))
    sequence.add_action(KeyAction(ActionType.KEY_RELEASE, "a", 0.1))
    sequence.add_action(KeyAction(ActionType.KEY_PRESS, "b", 0.2))
    sequence.add_action(KeyAction(ActionType.KEY_RELEASE, "b", 0.3))
    
    return sequence
