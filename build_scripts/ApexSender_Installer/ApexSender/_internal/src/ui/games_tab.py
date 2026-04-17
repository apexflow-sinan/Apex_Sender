"""Games Web Tab"""
import os
import threading
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPen, QBrush, QColor
import qtawesome as qta
import qrcode
from io import BytesIO
import random
from src.widgets.loading_indicator import LoadingIndicator
from src.utils.server_diagnostics import check_port_available, get_alternative_port

class GamesTab(QWidget):
    def __init__(self, settings_manager, log_message):
        super().__init__()
        self.settings_manager = settings_manager
        self.log_message = log_message
        self.server_thread = None
        self.server_running = False
        self.flask_app = None
        self.setup_ui()
        
        self.loading = LoadingIndicator(self)
        self.loading.hide()
    
    def setup_ui(self):
        """Setup user interface"""
        self.setStyleSheet("""
            GamesTab {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(102, 126, 234, 0.02),
                    stop:1 rgba(155, 89, 182, 0.02));
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("🎮 ألعاب الويب للأطفال")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.status_label = QLabel("الخادم متوقف")
        self.status_label.setStyleSheet("font-size: 16px; color: #e74c3c; margin: 10px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setVisible(False)
        layout.addWidget(self.qr_label)
        
        self.url_label = QLabel()
        self.url_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #3498db; margin: 10px; "
            "text-decoration: underline;"
        )
        self.url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.url_label.setVisible(False)
        self.url_label.setOpenExternalLinks(True)
        layout.addWidget(self.url_label)
        
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("تشغيل الخادم")
        self.start_btn.setIcon(qta.icon('fa5s.play', color='#27ae60'))
        self.start_btn.clicked.connect(self.start_session)
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
                min-width: 120px;
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
        self.stop_btn.clicked.connect(self.stop_session)
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
                min-width: 120px;
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
        
        info = QLabel("📱 امسح رمز QR أو افتح الرابط في متصفح الموبايل")
        info.setStyleSheet("color: #7f8c8d; margin: 20px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width, height = self.width(), self.height()
        random.seed(42)
        
        for i in range(15):
            x = random.randint(30, width - 30)
            y = random.randint(30, height - 30)
            angle = random.randint(-45, 45)
            size = random.randint(60, 100)
            
            # ألوان مختلفة
            colors = [
                QColor(102, 126, 234, 15),
                QColor(155, 89, 182, 15),
                QColor(52, 152, 219, 15),
                QColor(46, 204, 113, 15),
                QColor(241, 196, 15, 15)
            ]
            color = colors[i % len(colors)]
            painter.setPen(QPen(color, 2))
            painter.setBrush(QBrush(color))
            
            painter.save()
            painter.translate(x, y)
            painter.rotate(angle)
            
            if i % 3 == 0:
                painter.drawRoundedRect(-size//2, -size//2, size, size, 8.0, 8.0)
            elif i % 3 == 1:
                painter.drawEllipse(-size//2, -size//2, size, size)
            else:
                points = [
                    (0, -size//2),
                    (size//2, size//3),
                    (-size//2, size//3)
                ]
                from PyQt6.QtCore import QPoint
                painter.drawPolygon([QPoint(p[0], p[1]) for p in points])
            
            painter.restore()
    
    def start_session(self):
        """Start new gaming session"""
        import time
        import sys
        
        start_time = time.time()
        self.loading.show_indicator()
        self.start_btn.setEnabled(False)
        self.status_label.setText("جاري تشغيل الخادم...")
        self.status_label.setStyleSheet("font-size: 16px; color: #f39c12; margin: 10px;")
        
        try:
            port = self.settings_manager.get("games_port", 8080)
            
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
                        self.settings_manager.set("games_port", port)
                        self.log_message(f"تم التبديل للمنفذ {port}")
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
            
            # Get ApexGames directory (works with PyInstaller)
            if getattr(sys, 'frozen', False):
                # PyInstaller puts data in _MEIPASS
                if hasattr(sys, '_MEIPASS'):
                    games_dir = os.path.join(sys._MEIPASS, 'ApexGames')
                else:
                    games_dir = os.path.join(os.path.dirname(sys.executable), 'ApexGames')
                
                if not os.path.exists(games_dir):
                    raise FileNotFoundError(f"ApexGames not found at: {games_dir}")
            else:
                games_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ApexGames')
                if not os.path.exists(games_dir):
                    raise FileNotFoundError(f"ApexGames directory not found: {games_dir}")
            
            if games_dir not in sys.path:
                sys.path.insert(0, os.path.dirname(games_dir))
            
            os.environ['APEX_GAMES_PORT'] = str(port)
            
            # Import server module
            server_file = os.path.join(games_dir, 'server.py')
            if not os.path.exists(server_file):
                raise FileNotFoundError(f"server.py not found: {server_file}")
            
            import importlib.util
            spec = importlib.util.spec_from_file_location("apex_games_server", server_file)
            server_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(server_module)
            self.flask_app = server_module.app
            
            ip = self._get_selected_ip()
            url = f"http://{ip}:{port}"
            
            def run_server():
                import logging
                log = logging.getLogger('werkzeug')
                log.setLevel(logging.ERROR)
                from werkzeug.serving import make_server
                self.server = make_server('0.0.0.0', port, self.flask_app, threaded=True)
                self.server.serve_forever()
            
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            
            self.server_running = True
            self.status_label.setText("✅ الخادم يعمل")
            self.status_label.setStyleSheet("font-size: 16px; color: #27ae60; margin: 10px;")
            
            self.generate_qr_code(url)
            self.url_label.setText(f'<a href="{url}" style="color: #667eea; text-decoration: underline;">{url}</a>')
            self.qr_label.setVisible(True)
            self.url_label.setVisible(True)
            
            self.loading.hide_indicator()
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            
            elapsed = time.time() - start_time
            self.log_message(f"⚡ Games server started: {url} (في {elapsed:.2f} ثانية)")
        
        except Exception as e:
            import traceback
            error_msg = f"Failed to start games server: {e}\n{traceback.format_exc()}"
            self.log_message(error_msg)
            self.loading.hide_indicator()
            self.start_btn.setEnabled(True)
            self.status_label.setText("فشل التشغيل")
            self.status_label.setStyleSheet("font-size: 14px; color: #e74c3c; margin: 10px;")
            QMessageBox.critical(self, "خطأ في تشغيل الخادم", f"فشل تشغيل الخادم:\n\n{str(e)}")
    
    def _get_selected_ip(self):
        """Get IP from main window header network selector"""
        main = self.window()
        if hasattr(main, 'get_selected_ip'):
            return main.get_selected_ip()
        from src.utils.network_utils import get_local_ip
        return get_local_ip()
    
    def stop_session(self):
        """Stop current session and server"""
        import time
        
        start_time = time.time()
        self.loading.show_indicator()
        
        try:
            if hasattr(self, 'server'):
                self.server.shutdown()
        except:
            pass
        finally:
            self.loading.hide_indicator()
            elapsed = time.time() - start_time
        
        self.server_running = False
        self.status_label.setText("الخادم متوقف")
        self.status_label.setStyleSheet("font-size: 16px; color: #e74c3c; margin: 10px;")
        self.qr_label.setVisible(False)
        self.url_label.setVisible(False)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        self.log_message(f"⚡ Games server stopped (في {elapsed:.2f} ثانية)")
    
    def generate_qr_code(self, url):
        """Generate QR code for URL"""
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.read())
        scaled_pixmap = pixmap.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.qr_label.setPixmap(scaled_pixmap)
    
    def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'server_running') and self.server_running:
            try:
                if hasattr(self, 'server'):
                    self.server.shutdown()
            except:
                pass
