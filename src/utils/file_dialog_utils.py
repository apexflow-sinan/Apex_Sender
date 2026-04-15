"""Custom file dialog utilities for better drive visibility on Linux"""
import os
import sys
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QUrl

def get_linux_drives():
    """Get list of mounted drives on Linux"""
    drives = []
    
    # Common mount points
    mount_points = ['/media', '/mnt', '/run/media']
    
    # Add home directory
    drives.append(('🏠 المجلد الرئيسي', os.path.expanduser('~')))
    
    # Add root
    drives.append(('💾 الجذر', '/'))
    
    # Scan mount points
    for mount_base in mount_points:
        if os.path.exists(mount_base):
            try:
                for user_dir in os.listdir(mount_base):
                    user_path = os.path.join(mount_base, user_dir)
                    if os.path.isdir(user_path):
                        for drive in os.listdir(user_path):
                            drive_path = os.path.join(user_path, drive)
                            if os.path.isdir(drive_path):
                                drives.append((f'💿 {drive}', drive_path))
            except (PermissionError, OSError):
                pass
    
    return drives

_HOME = os.path.expanduser('~')


def get_open_filename(parent, title, start_dir=""):
    """Open file dialog with drive shortcuts on Linux"""
    if not start_dir:
        start_dir = _HOME
    if sys.platform.startswith('linux'):
        dialog = QFileDialog(parent, title)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        
        # Add drive shortcuts
        urls = dialog.sidebarUrls()
        for name, path in get_linux_drives():
            if os.path.exists(path):
                urls.append(QUrl.fromLocalFile(path))
        dialog.setSidebarUrls(urls)
        
        if start_dir and os.path.exists(start_dir):
            dialog.setDirectory(start_dir)
        
        if dialog.exec():
            return dialog.selectedFiles()[0], None
        return None, None
    else:
        return QFileDialog.getOpenFileName(parent, title, start_dir)

def get_open_filenames(parent, title, start_dir=""):
    """Open multiple files dialog with drive shortcuts on Linux"""
    if not start_dir:
        start_dir = _HOME
    if sys.platform.startswith('linux'):
        dialog = QFileDialog(parent, title)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        
        # Add drive shortcuts
        urls = dialog.sidebarUrls()
        for name, path in get_linux_drives():
            if os.path.exists(path):
                urls.append(QUrl.fromLocalFile(path))
        dialog.setSidebarUrls(urls)
        
        if start_dir and os.path.exists(start_dir):
            dialog.setDirectory(start_dir)
        
        if dialog.exec():
            return dialog.selectedFiles(), None
        return [], None
    else:
        return QFileDialog.getOpenFileNames(parent, title, start_dir)

def get_existing_directory(parent, title, start_dir=""):
    """Open directory dialog with drive shortcuts on Linux"""
    if not start_dir:
        start_dir = _HOME
    if sys.platform.startswith('linux'):
        dialog = QFileDialog(parent, title)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        
        # Add drive shortcuts
        urls = dialog.sidebarUrls()
        for name, path in get_linux_drives():
            if os.path.exists(path):
                urls.append(QUrl.fromLocalFile(path))
        dialog.setSidebarUrls(urls)
        
        if start_dir and os.path.exists(start_dir):
            dialog.setDirectory(start_dir)
        
        if dialog.exec():
            return dialog.selectedFiles()[0]
        return None
    else:
        return QFileDialog.getExistingDirectory(parent, title, start_dir)
