"""QR Code dialog"""
import qtawesome as qta
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from src.utils.qr_utils import generate_qr_code, create_connection_url

class QRDialog(QDialog):
    """QR Code display dialog"""
    
    def __init__(self, parent, ip, port):
        super().__init__(parent)
        self.ip = ip
        self.port = port
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("QR Code - Apex Sender")
        self.setFixedSize(350, 450)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("مسح الرمز للاتصال")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # QR Code
        url = create_connection_url(self.ip, self.port)
        qr_data = generate_qr_code(url, (250, 250))
        
        qr_label = QLabel()
        image = QImage.fromData(qr_data)
        pixmap = QPixmap.fromImage(image)
        qr_label.setPixmap(pixmap)
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(qr_label)
        
        # URL text
        url_text = QTextEdit()
        url_text.setPlainText(url)
        url_text.setMaximumHeight(60)
        url_text.setReadOnly(True)
        layout.addWidget(url_text)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        copy_btn = QPushButton(qta.icon('fa5s.copy'), " نسخ الرابط")
        copy_btn.clicked.connect(self.copy_url)
        btn_layout.addWidget(copy_btn)
        
        close_btn = QPushButton(qta.icon('fa5s.times'), " إغلاق")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def copy_url(self):
        """Copy URL to clipboard"""
        from PyQt6.QtWidgets import QApplication
        url = create_connection_url(self.ip, self.port)
        QApplication.clipboard().setText(url)

def show_qr_dialog(parent, ip, port):
    """Show QR dialog"""
    dialog = QRDialog(parent, ip, port)
    dialog.exec()