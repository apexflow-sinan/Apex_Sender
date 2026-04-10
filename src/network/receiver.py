"""File receiver thread"""
import socket
import time
from PyQt6.QtCore import QObject
from src.network.signals import WorkerSignals
from src.config.settings import BUFFER_SIZE
from src.utils.file_utils import get_unique_filename

class ReceiverThread(QObject):
    """Thread for receiving files"""
    signals = WorkerSignals()
    
    def __init__(self, port, save_dir):
        super().__init__()
        self.port = port
        self.save_dir = save_dir
        self.is_running = True
    
    def stop(self):
        """Stop the receiver"""
        self.is_running = False
    
    def run(self):
        """Run the receiver thread"""
        while self.is_running:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.settimeout(1.0)
                    s.bind(('', self.port))
                    s.listen(5)
                    self.signals.log_message.emit(f"الاستماع على البورت {self.port}...")
                    
                    while self.is_running:
                        try:
                            conn, addr = s.accept()
                            if not self.is_running:
                                conn.close()
                                break
                            
                            self._receive_file(conn, addr)
                        
                        except socket.timeout:
                            continue
                        except Exception as e:
                            if self.is_running:
                                self.signals.log_message.emit(f"خطأ: {e}")
            
            except Exception as e:
                if self.is_running:
                    self.signals.log_message.emit(f"خطأ في الخادم: {e}")
                    time.sleep(2)
    
    def _receive_file(self, conn, addr):
        """Receive a single file"""
        self.signals.log_message.emit(f"اتصال وارد من {addr[0]}")
        
        with conn:
            # Optimize socket for speed
            conn.settimeout(30.0)
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 * 1024 * 1024)  # 2MB
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Disable Nagle
            
            # Read header
            header_parts = []
            header_buffer = b""
            
            while len(header_parts) < 2:
                try:
                    chunk = conn.recv(64)
                    if not chunk:
                        break
                    header_buffer += chunk
                    if b'\n' in header_buffer:
                        parts = header_buffer.split(b'\n', 1)
                        header_parts.append(parts[0].decode())
                        header_buffer = parts[1]
                except socket.timeout:
                    self.signals.log_message.emit("انتهى وقت الانتظار")
                    return
            
            if len(header_parts) < 2:
                self.signals.log_message.emit("فشل استقبال معلومات الملف")
                return
            
            filename = header_parts[0]
            file_size = int(header_parts[1])
            
            save_path = get_unique_filename(self.save_dir, filename)
            
            # Receive file
            with open(save_path, 'wb') as f:
                f.write(header_buffer)
                received = len(header_buffer)
                start_time = time.time()
                last_data_time = time.time()
                
                # Use larger buffer for faster receiving
                chunk_size = 256 * 1024  # 256KB
                while received < file_size:
                    try:
                        data = conn.recv(min(chunk_size, file_size - received))
                        if not data:
                            break
                        
                        f.write(data)
                        received += len(data)
                        last_data_time = time.time()
                        
                        elapsed = time.time() - start_time
                        speed = (received / 1024 / 1024) / elapsed if elapsed > 0 else 0
                        progress = (received / file_size) * 100
                        status = f"{received/1024/1024:.2f} MB / {file_size/1024/1024:.2f} MB"
                        
                        self.signals.progress_update.emit(int(progress), status, speed)
                    
                    except socket.timeout:
                        # Check if we've been waiting too long
                        if time.time() - last_data_time > 30:
                            self.signals.log_message.emit("انتهى وقت الانتظار أثناء الاستقبال")
                            break
                        continue
            
            if received == file_size:
                # Check if it's a text message
                if filename == '__APEX_TEXT__':
                    try:
                        import os as _os
                        with open(save_path, 'r', encoding='utf-8') as tf:
                            text_content = tf.read()
                        _os.remove(save_path)
                        self.signals.text_received.emit(text_content)
                        self.signals.log_message.emit("تم استقبال رسالة نصية")
                    except:
                        self.signals.file_received.emit(filename, save_path)
                else:
                    self.signals.log_message.emit(f"تم حفظ {filename}")
                    self.signals.file_received.emit(filename, save_path)
                
                # Check if sender is from same device
                from src.utils.network_utils import get_local_ip
                local_ip = get_local_ip()
                sender_ip = addr[0]
                is_same_device = (sender_ip == local_ip or sender_ip == '127.0.0.1' or sender_ip == 'localhost')
                
                # Only show success message if from different device
                if not is_same_device:
                    self.signals.task_finished.emit("تم الاستقبال بنجاح!")
                
                # Only ask to extract if sender is from different device
                if filename.lower().endswith('.zip') and not is_same_device:
                    self.signals.ask_extract.emit(save_path)
            else:
                self.signals.task_finished.emit("فشل الاستقبال: اتصال غير مكتمل")
