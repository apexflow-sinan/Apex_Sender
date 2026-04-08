"""Settings manager for persistent storage"""
import json
import os
from pathlib import Path
from .platform_manager import PlatformManager
from src.config.settings import DEFAULT_SAVE_DIR

class SettingsManager:
    def __init__(self):
        try:
            # Create platform-specific directories
            PlatformManager.create_directories()
            self.settings_file = PlatformManager.get_config_dir() / "settings.json"
        except Exception as e:
            # Fallback to home directory if there's an error
            print(f"Warning: Could not create config directory: {e}")
            self.settings_file = Path.home() / "ApexSender" / "settings.json"
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        default_settings = {
            "save_directory": DEFAULT_SAVE_DIR,
            "dark_mode": True,
            "sound_enabled": True,
            "ip_history": [],
            "auto_extract_zip": True
        }
        
        try:
            if self.settings_file.exists():
                try:
                    with open(self.settings_file, 'r', encoding='utf-8') as f:
                        loaded = json.load(f)
                        default_settings.update(loaded)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Could not load settings: {e}")
        except Exception as e:
            print(f"Warning: Error checking settings file: {e}")
        
        return default_settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            # Ensure directory exists
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except (IOError, OSError, PermissionError) as e:
            print(f"Error saving settings: {e}")
        except Exception as e:
            print(f"Unexpected error saving settings: {e}")
    
    def get(self, key, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def add_ip_to_history(self, ip):
        """Add IP to history"""
        history = self.settings.get("ip_history", [])
        if ip in history:
            history.remove(ip)
        history.insert(0, ip)
        self.settings["ip_history"] = history[:10]  # Keep last 10
        self.save_settings()
