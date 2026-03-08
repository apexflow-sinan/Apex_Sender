"""File utility functions"""
import os
import zipfile
import tempfile

def compress_folder(folder_path, progress_callback=None):
    """Compress folder to temporary zip file with progress callback"""
    zip_path = tempfile.mktemp(suffix='.zip')
    folder_name = os.path.basename(folder_path)
    
    # Files to ignore
    ignore_files = {'.apex_history.json', '.DS_Store', 'Thumbs.db', 'desktop.ini'}
    
    # Count total files for progress (excluding hidden/system files)
    total_files = 0
    for root, dirs, files in os.walk(folder_path):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.startswith('.') and file not in ignore_files:
                total_files += 1
    
    if progress_callback:
        progress_callback(0, f"عد الملفات: {total_files}")
    
    processed_files = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                # Skip hidden files and system files
                if file.startswith('.') or file in ignore_files:
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.join(folder_name, os.path.relpath(file_path, folder_path))
                zipf.write(file_path, arcname)
                processed_files += 1
                
                if progress_callback and total_files > 0:
                    progress = int((processed_files / total_files) * 100)
                    progress_callback(progress, f"ضغط: {processed_files}/{total_files}")
    
    return zip_path

def extract_zip(zip_path):
    """Extract zip file to folder with same name"""
    extract_dir = os.path.splitext(zip_path)[0]
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_dir)
    return extract_dir

def get_unique_filename(directory, filename):
    """Get unique filename if file already exists"""
    save_path = os.path.join(directory, filename)
    
    if not os.path.exists(save_path):
        return save_path
    
    name, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(save_path):
        save_path = os.path.join(directory, f"{name}_{counter}{ext}")
        counter += 1
    
    return save_path

def format_size(size_bytes):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def calculate_speed(bytes_transferred, elapsed_time):
    """Calculate transfer speed in MB/s"""
    if elapsed_time == 0:
        return 0
    return (bytes_transferred / 1024 / 1024) / elapsed_time
