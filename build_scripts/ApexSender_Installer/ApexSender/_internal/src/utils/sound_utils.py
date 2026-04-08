"""Sound utility functions"""
import os
import sys

def play_success_sound():
    """Play success sound"""
    try:
        if os.name == 'nt':  # Windows
            import winsound
            winsound.MessageBeep(winsound.MB_OK)
    except ImportError:
        pass

def play_error_sound():
    """Play error sound"""
    try:
        if os.name == 'nt':  # Windows
            import winsound
            winsound.MessageBeep(winsound.MB_ICONHAND)
    except ImportError:
        pass

def play_notification_sound():
    """Play notification sound"""
    try:
        if os.name == 'nt':  # Windows
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except ImportError:
        pass