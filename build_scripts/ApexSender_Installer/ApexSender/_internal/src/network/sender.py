"""File sender thread"""
import os
import socket
import time
from PyQt6.QtCore import QObject
from src.network.signals import WorkerSignals
from src.config.settings import BUFFER_SIZE

class SenderThread(QObject):
    """Thread for sending files"""
    signals = WorkerSignals()
    
    def __init__(self, host, port, file_paths):
        super().__init__()
        self.host = host
        self.port = port
        self.file_paths = file_paths if isinstance(file_paths, list) else [file_paths]
        self.is_cancelled = False
    
    def cancel(self):
        """Cancel the transfer"""
        self.is_cancelled = True
    
    def run(self):
        """Run the sender thread"""
        try:
            for file_path in self.file_paths:
                if self.is_cancelled:
                    self.signals.task_finished.emit("تم إلغاء الإرسال")
                    return
                
                self._send_file(file_path)
            
            self.signals.task_finished.emit("تم الإرسال بنجاح!")
        except ConnectionRefusedError:
            self.signals.task_finished.emit(f"فشل الإرسال: لم يتم العثور على المستقبل على {self.host}")
        except socket.timeout:
            self.signals.task_finished.emit("فشل الإرسال: انتهى وقت الاتصال")
        except Exception as e:
            self.signals.task_finished.emit(f"فشل الإرسال: {e}")
    
    def _send_file(self, file_path):
        """Send a single file"""
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        self.signals.log_message.emit(f"بدء إرسال {filename} إلى {self.host}...")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)  # Increased timeout for connection
            s.connect((self.host, self.port))
            s.settimeout(30)  # Longer timeout for data transfer
            s.sendall(f"{filename}\n{file_size}\n".encode())
            
            sent = 0
            start_time = time.time()
            
            with open(file_path, 'rb') as f:
                while sent < file_size and not self.is_cancelled:
                    data = f.read(BUFFER_SIZE)
                    if not data:
                        break
                    
                    try:
                        s.sendall(data)
                        sent += len(data)
                        
                        elapsed = time.time() - start_time
                        speed = (sent / 1024 / 1024) / elapsed if elapsed > 0 else 0
                        progress = (sent / file_size) * 100
                        status = f"{sent/1024/1024:.2f} MB / {file_size/1024/1024:.2f} MB"
                        
                        self.signals.progress_update.emit(int(progress), status, speed)
                    
                    except socket.timeout:
                        raise Exception("انتهى وقت الإرسال")
                    except socket.error as e:
                        raise Exception(f"خطأ في الشبكة: {e}")
        
        if not self.is_cancelled:
            self.signals.log_message.emit(f"تم إرسال {filename} بنجاح")
