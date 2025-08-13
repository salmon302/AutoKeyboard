"""
Version information for AutoKeyboard.
"""

__version__ = "1.2.0"
__author__ = "AutoKeyboard Project"
__email__ = "contact@autokeyboard.dev"
__description__ = "A powerful keyboard automation tool with recording and playback capabilities"
__url__ = "https://github.com/salmon302/AutoKeyboard"

# Version components
VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_PATCH = 0
VERSION_SUFFIX = ""  # e.g., "beta", "alpha", "rc1"

# Build information
BUILD_DATE = "2025-08-13"
BUILD_PLATFORM = "Windows"

def get_version_string():
    """Get the complete version string."""
    version = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
    if VERSION_SUFFIX:
        version += f"-{VERSION_SUFFIX}"
    return version

def get_version_info():
    """Get version information as a dictionary."""
    return {
        "version": get_version_string(),
        "major": VERSION_MAJOR,
        "minor": VERSION_MINOR,
        "patch": VERSION_PATCH,
        "suffix": VERSION_SUFFIX,
        "build_date": BUILD_DATE,
        "build_platform": BUILD_PLATFORM,
    }

# For backward compatibility
version = __version__
