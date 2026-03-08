"""Apex Sender Version Information"""

__version__ = "2.0.0"
__version_info__ = (2, 0, 0)
__app_name__ = "Apex Sender"
__author__ = "Apex Development Team"
__copyright__ = "Copyright © 2024 Apex Development Team"
__license__ = "Proprietary"
__description__ = "Fast and secure file transfer application"

# Build information
BUILD_DATE = "2024-01-15"
BUILD_TYPE = "Release"

# Version history
VERSION_HISTORY = {
    "2.0.0": {
        "date": "2024-01-15",
        "changes": [
            "Added web interface for mobile access",
            "Implemented Windows Service support",
            "Added advanced settings dialog",
            "Improved firewall configuration",
            "Enhanced UI with dark mode",
            "Added QR code sharing",
            "Optimized file transfer speed"
        ]
    },
    "1.0.0": {
        "date": "2023-12-01",
        "changes": [
            "Initial release",
            "Basic file transfer functionality",
            "Sender and receiver tabs",
            "IP history management"
        ]
    }
}

def get_version_string():
    """Get formatted version string"""
    return f"{__app_name__} v{__version__}"

def get_full_version_info():
    """Get complete version information"""
    return {
        "app_name": __app_name__,
        "version": __version__,
        "build_date": BUILD_DATE,
        "build_type": BUILD_TYPE,
        "author": __author__,
        "copyright": __copyright__,
        "description": __description__
    }
