"""Qt Signals for network operations"""
from PyQt6.QtCore import QObject, pyqtSignal

class WorkerSignals(QObject):
    """Signals for worker threads"""
    log_message = pyqtSignal(str)
    progress_update = pyqtSignal(int, str, float)  # progress, status, speed
    task_finished = pyqtSignal(str)
    ask_extract = pyqtSignal(str)
    show_success = pyqtSignal(str, str)
    show_error = pyqtSignal(str, str)
    transfer_complete = pyqtSignal(bool, str, str)  # success, message, ip
    file_received = pyqtSignal(str, str)  # filename, filepath
    text_received = pyqtSignal(str)  # text content
