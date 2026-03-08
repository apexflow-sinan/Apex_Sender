"""About dialog"""
import qtawesome as qta
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.core.settings_manager import SettingsManager
from src.version import __version__, __app_name__, __copyright__, BUILD_DATE

class AboutDialog(QDialog):
    """Beautiful about dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = SettingsManager()
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("حول Apex Sender")
        self.setFixedSize(450, 500)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.rocket', color='#667eea').pixmap(80, 80))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title
        title = QLabel(f"⚡ {__app_name__}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #667eea;")
        layout.addWidget(title)
        
        # Version
        version = QLabel(f"v{__version__} | {BUILD_DATE}")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        layout.addWidget(version)
        
        # Description
        desc = QLabel("تطبيق نقل الملفات السريع والآمن\nبين الأجهزة على نفس الشبكة")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setObjectName("descLabel")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Features
        features_box = QVBoxLayout()
        features_box.setSpacing(10)
        
        features = [
            ("fa5s.bolt", "نقل سريع وآمن"),
            ("fa5s.mobile-alt", "دعم الهاتف عبر الويب"),
            ("fa5s.qrcode", "مسح QR للاتصال السريع"),
            ("fa5s.shield-alt", "تشفير آمن"),
            ("fa5s.palette", "واجهة جميلة وسهلة"),
        ]
        
        for icon_name, text in features:
            feature_layout = QHBoxLayout()
            feature_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            
            icon = QLabel()
            icon.setPixmap(qta.icon(icon_name, color='#27ae60').pixmap(20, 20))
            
            label = QLabel(text)
            label.setObjectName("featureLabel")
            
            feature_layout.addWidget(label)
            feature_layout.addWidget(icon)
            features_box.addLayout(feature_layout)
        
        layout.addLayout(features_box)
        
        layout.addStretch()
        
        # Footer
        footer = QLabel(f"{__copyright__}\nجميع الحقوق محفوظة")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #95a5a6; font-size: 11px;")
        layout.addWidget(footer)
        
        # Close button
        close_btn = QPushButton(qta.icon('fa5s.times'), " إغلاق")
        close_btn.clicked.connect(self.close)
        close_btn.setObjectName("primaryButton")
        layout.addWidget(close_btn)
    
    def apply_theme(self):
        """Apply theme based on settings"""
        is_dark = self.settings_manager.get("dark_mode", False)
        
        if is_dark:
            self.setStyleSheet("""
                QDialog {
                    background: #1e1e2e;
                    color: #cdd6f4;
                }
                QLabel {
                    color: #cdd6f4;
                }
                QLabel#descLabel {
                    color: #bac2de;
                    font-size: 13px;
                }
                QLabel#featureLabel {
                    color: #cdd6f4;
                    font-size: 12px;
                }
                QPushButton#primaryButton {
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 10px 30px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#primaryButton:hover {
                    background: #5568d3;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background: white;
                    color: #2c3e50;
                }
                QLabel#descLabel {
                    color: #2c3e50;
                    font-size: 13px;
                }
                QLabel#featureLabel {
                    color: #34495e;
                    font-size: 12px;
                }
                QPushButton#primaryButton {
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 10px 30px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#primaryButton:hover {
                    background: #5568d3;
                }
            """)
