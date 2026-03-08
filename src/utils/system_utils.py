"""System utilities for cross-platform operations"""
import os
import sys
import subprocess

def open_file_or_folder(path):
    """
    Open file or folder in system file manager (cross-platform)
    
    Args:
        path: Path to file or folder
        
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    if not os.path.exists(path):
        return False, "المسار غير موجود"
    
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", path], check=True)
        else:  # Linux and others
            subprocess.run(["xdg-open", path], check=True)
        return True, None
    except Exception as e:
        return False, str(e)
