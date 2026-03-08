"""
Platform Manager - Cross-platform compatibility layer
"""
import platform
import sys
import os
from pathlib import Path

class PlatformManager:
    """Manages platform-specific operations"""
    
    @staticmethod
    def get_platform():
        """Get current platform"""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system == "darwin":
            return "macos"
        elif system == "linux":
            return "linux"
        else:
            return "unknown"
    
    @staticmethod
    def is_windows():
        return PlatformManager.get_platform() == "windows"
    
    @staticmethod
    def is_macos():
        return PlatformManager.get_platform() == "macos"
    
    @staticmethod
    def is_linux():
        return PlatformManager.get_platform() == "linux"
    
    @staticmethod
    def get_config_dir():
        """Get platform-specific config directory"""
        platform_name = PlatformManager.get_platform()
        
        if platform_name == "windows":
            return Path.home() / "AppData" / "Local" / "ApexSender"
        elif platform_name == "macos":
            return Path.home() / "Library" / "Application Support" / "ApexSender"
        else:  # Linux
            return Path.home() / ".config" / "ApexSender"
    
    @staticmethod
    def get_data_dir():
        """Get platform-specific data directory"""
        platform_name = PlatformManager.get_platform()
        
        if platform_name == "windows":
            return Path.home() / "AppData" / "Local" / "ApexSender"
        elif platform_name == "macos":
            return Path.home() / "Library" / "Application Support" / "ApexSender"
        else:  # Linux
            return Path.home() / ".local" / "share" / "ApexSender"
    
    @staticmethod
    def get_temp_dir():
        """Get platform-specific temp directory"""
        return Path.home() / "tmp" / "ApexSender" if not PlatformManager.is_windows() else Path.home() / "AppData" / "Local" / "Temp" / "ApexSender"
    
    @staticmethod
    def create_directories():
        """Create necessary directories"""
        try:
            dirs = [
                PlatformManager.get_config_dir(),
                PlatformManager.get_data_dir(),
                PlatformManager.get_temp_dir()
            ]
            
            for dir_path in dirs:
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                except (OSError, PermissionError) as e:
                    # If we can't create a directory, try to continue with others
                    print(f"Warning: Could not create directory {dir_path}: {e}")
        except Exception as e:
            print(f"Warning: Error creating directories: {e}")
    
    @staticmethod
    def get_executable_extension():
        """Get executable extension for current platform"""
        return ".exe" if PlatformManager.is_windows() else ""
    
    @staticmethod
    def supports_services():
        """Check if platform supports background services"""
        return True  # All platforms support some form of background services