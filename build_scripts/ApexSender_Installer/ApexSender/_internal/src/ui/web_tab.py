"""Web Access tab"""
import os
import sys
import threading
import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
)
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from src.utils.network_utils import get_local_ip
from src.utils.qr_utils import generate_qr_code
from src.widgets.loading_indicator import LoadingIndicator
from src.utils.server_diagnostics import check_port_available, get_alternative_port

class WebTab(QWidget):
    """Web access tab widget"""
    
    def __init__(self, settings_manager, log_callback):
        super().__init__()
        self.settings_manager = settings_manager
        self.log_callback = log_callback
        self.server_thread = None
        self.server_running = False
        self.setup_ui()
        
        # Loading indicator
        self.loading = LoadingIndicator(self)
        self.loading.hide()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel("🌐 الوصول عبر الويب")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Status
        self.status_label = QLabel("الخادم متوقف")
        self.status_label.setStyleSheet("font-size: 16px; color: #e74c3c; margin: 10px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # QR Code
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setVisible(False)
        layout.addWidget(self.qr_label)
        
        # URL (clickable)
        self.url_label = QLabel()
        self.url_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #3498db; margin: 10px; "
            "text-decoration: underline;"
        )
        self.url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.url_label.setVisible(False)
        self.url_label.setOpenExternalLinks(True)
        layout.addWidget(self.url_label)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("تشغيل الخادم")
        self.start_btn.setIcon(qta.icon('fa5s.play', color='#27ae60'))
        self.start_btn.clicked.connect(self.start_server)
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #27ae60;
                color: #27ae60;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #27ae60;
                color: white;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
        """)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("إيقاف الخادم")
        self.stop_btn.setIcon(qta.icon('fa5s.stop', color='#e74c3c'))
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #e74c3c;
                color: #e74c3c;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:pressed {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                border-color: #95a5a6;
                color: #95a5a6;
                background-color: transparent;
            }
        """)
        btn_layout.addWidget(self.stop_btn)
        
        layout.addLayout(btn_layout)
        
        # Info
        info = QLabel("📱 امسح رمز QR أو افتح الرابط في متصفح الموبايل")
        info.setStyleSheet("color: #7f8c8d; margin: 20px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
    
    def start_server(self):
        """Start web server"""
        import time
        start_time = time.time()
        
        # Show loading
        self.loading.show_indicator()
        self.start_btn.setEnabled(False)
        self.status_label.setText("جاري تشغيل الخادم...")
        self.status_label.setStyleSheet("font-size: 16px; color: #f39c12; margin: 10px;")
        
        try:
            port = self.settings_manager.get("web_port", 5000)
            
            # فحص المنفذ
            port_ok, port_msg = check_port_available(port)
            if not port_ok:
                alt_port = get_alternative_port(port)
                if alt_port:
                    reply = QMessageBox.question(
                        self, "المنفذ مستخدم",
                        f"المنفذ {port} مستخدم.\n\nهل تريد استخدام المنفذ {alt_port}؟",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        port = alt_port
                        self.settings_manager.set("web_port", port)
                        self.log_callback(f"تم التبديل للمنفذ {port}")
                    else:
                        self.loading.hide_indicator()
                        self.start_btn.setEnabled(True)
                        self.status_label.setText("تم الإلغاء")
                        self.status_label.setStyleSheet("font-size: 16px; color: #e74c3c; margin: 10px;")
                        return
                else:
                    self.loading.hide_indicator()
                    self.start_btn.setEnabled(True)
                    self.status_label.setText("فشل التشغيل")
                    self.status_label.setStyleSheet("font-size: 16px; color: #e74c3c; margin: 10px;")
                    QMessageBox.critical(self, "فشل التشغيل", f"{port_msg}\n\nلا يوجد منافذ بديلة.")
                    return
            
            # Add project root to path
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            
            from web.server import start_server
            
            ip = get_local_ip()
            url = f"http://{ip}:{port}"
            
            # Start server in thread
            self.server_thread = threading.Thread(
                target=start_server, 
                args=(port,), 
                daemon=True
            )
            self.server_thread.start()
            
            # Update UI
            self.server_running = True
            self.status_label.setText("✅ الخادم يعمل")
            self.status_label.setStyleSheet("font-size: 16px; color: #27ae60; margin: 10px;")
            
            # Show QR (smaller size)
            qr_data = generate_qr_code(url, (180, 180))
            image = QImage.fromData(qr_data)
            qr_pixmap = QPixmap.fromImage(image)
            self.qr_label.setPixmap(qr_pixmap)
            self.qr_label.setVisible(True)
            
            # Show URL (clickable)
            self.url_label.setText(f'<a href="{url}" style="color: #3498db;">{url}</a>')
            self.url_label.setVisible(True)
            self.current_url = url
            
            # Update buttons
            self.loading.hide_indicator()
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            
            elapsed = time.time() - start_time
            self.log_callback(f"⚡ Web server started: {url} (في {elapsed:.2f} ثانية)")
        
        except Exception as e:
            import traceback
            error_msg = f"Failed to start web server: {e}\n{traceback.format_exc()}"
            self.log_callback(error_msg)
            self.loading.hide_indicator()
            self.start_btn.setEnabled(True)
            self.status_label.setText("فشل التشغيل")
            self.status_label.setStyleSheet("font-size: 14px; color: #e74c3c; margin: 10px;")
            
            # عرض رسالة خطأ مفصلة
            error_details = str(e)
            if "Address already in use" in error_details or "WinError 10048" in error_details:
                error_details = f"المنفذ {port} مستخدم من برنامج آخر"
            
            QMessageBox.critical(
                self,
                "خطأ في تشغيل الخادم",
                f"فشل تشغيل الخادم:\n\n{error_details}\n\nتحقق من:\n• المنفذ غير مستخدم\n• تثبيت Flask\n• صلاحيات جدار الحماية"
            )
    
    def stop_server(self):
        """Stop web server"""
        import time
        start_time = time.time()
        
        self.loading.show_indicator()
        try:
            port = self.settings_manager.get("web_port", 5000)
            requests.post(f'http://127.0.0.1:{port}/shutdown', timeout=2)
        except:
            pass
        finally:
            self.loading.hide_indicator()
            elapsed = time.time() - start_time
        
        # Update UI
        self.server_running = False
        self.status_label.setText("الخادم متوقف")
        self.status_label.setStyleSheet("font-size: 16px; color: #e74c3c; margin: 10px;")
        self.qr_label.setVisible(False)
        self.url_label.setVisible(False)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        self.log_callback(f"⚡ Web server stopped (في {elapsed:.2f} ثانية)")
