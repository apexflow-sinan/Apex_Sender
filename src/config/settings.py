"""Application settings and constants"""
import os
import sys
from pathlib import Path
from src.version import __version__, __app_name__

# Network settings
DEFAULT_PORT = 8888
DEFAULT_WEB_PORT = 5000
DEFAULT_GAMES_PORT = 8080
BUFFER_SIZE = 65536  # 64KB for faster transfer
CONNECTION_TIMEOUT = 3

# Get base path (works with PyInstaller)
def get_base_path():
    try:
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller temp folder
                return sys._MEIPASS
            else:
                # Fallback to executable directory
                return os.path.dirname(sys.executable)
        else:
            # Running as script
            return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    except Exception:
        # Fallback to current directory
        return os.getcwd()

# Get user data directory (cross-platform)
def get_user_data_dir():
    """Get platform-specific user data directory"""
    try:
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            user_dir = Path.home() / "AppData" / "Local" / "ApexSender"
        elif system == "darwin":  # macOS
            user_dir = Path.home() / "Library" / "Application Support" / "ApexSender"
        else:  # Linux and others
            user_dir = Path.home() / ".local" / "share" / "ApexSender"
        
        user_dir.mkdir(parents=True, exist_ok=True)
        return str(user_dir)
    except Exception as e:
        # Fallback to home directory if there's any error
        fallback_dir = Path.home() / "ApexSender"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        return str(fallback_dir)

# Paths
APP_DIR = get_base_path()
USER_DATA_DIR = get_user_data_dir()
ASSETS_DIR = os.path.join(APP_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
# Get platform-specific default save directory
def get_default_save_dir():
    """Get platform-specific default save directory"""
    try:
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            save_dir = Path.home() / "Documents" / "ApexSender"
        elif system == "darwin":  # macOS
            save_dir = Path.home() / "Downloads" / "ApexSender"
        else:  # Linux and others
            save_dir = Path.home() / "Downloads" / "ApexSender"
        
        save_dir.mkdir(parents=True, exist_ok=True)
        return str(save_dir)
    except Exception as e:
        # Fallback to home directory if there's any error
        fallback_dir = Path.home() / "ApexSender"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        return str(fallback_dir)

DEFAULT_SAVE_DIR = get_default_save_dir()

# Files (store in user directory, not in exe)
HISTORY_FILE = os.path.join(USER_DATA_DIR, "history.json")

# Get platform-specific icon file
def get_icon_file():
    """Get icon file path"""
    try:
        # Try Icon.png first
        icon_path = os.path.join(ASSETS_DIR, "icons", "Icon.png")
        if os.path.exists(icon_path):
            return icon_path
        # Fallback to .ico
        icon_path = os.path.join(ASSETS_DIR, "icons", "Icon.ico")
        if os.path.exists(icon_path):
            return icon_path
        return ""
    except Exception:
        return ""

ICON_FILE = get_icon_file()

# UI Settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
ANIMATION_DURATION = 500

# Application Info
APP_NAME = __app_name__
APP_VERSION = __version__

# Features
ENABLE_SOUND = True
ENABLE_QR_CODE = True
ENABLE_DARK_MODE = True
