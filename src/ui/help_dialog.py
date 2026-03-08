"""Help and tips dialog"""
import qtawesome as qta
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QWidget, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.core.settings_manager import SettingsManager

class HelpDialog(QDialog):
    """Beautiful help dialog with tips"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = SettingsManager()
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("التعليمات والنصائح")
        self.setFixedSize(550, 600)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("📚 التعليمات والنصائح")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #667eea; padding: 15px;")
        layout.addWidget(header)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # Tips sections
        sections = [
            {
                "title": "🚀 البدء السريع",
                "tips": [
                    "تأكد من اتصال الجهازين بنفس الشبكة",
                    "استخدم تبويب 'إرسال' لإرسال الملفات",
                    "استخدم تبويب 'استقبال' لاستقبال الملفات",
                    "يمكنك استخدام الهاتف عبر تبويب 'Web'"
                ]
            },
            {
                "title": "📱 الإرسال من الهاتف",
                "tips": [
                    "افتح تبويب Web في البرنامج",
                    "اضغط 'تشغيل الخادم'",
                    "امسح رمز QR بالهاتف أو اكتب الرابط",
                    "اختر الملف وأدخل IP الجهاز المستقبل"
                ]
            },
            {
                "title": "⚡ نصائح لسرعة أعلى",
                "tips": [
                    "استخدم WiFi 5GHz بدلاً من 2.4GHz",
                    "قرّب الأجهزة من الراوتر",
                    "أغلق البرامج التي تستهلك الشبكة",
                    "تأكد من عدم وجود حواجز بين الأجهزة"
                ]
            },
            {
                "title": "🔒 الأمان",
                "tips": [
                    "استخدم شبكة WiFi موثوقة",
                    "لا تشارك IP الخاص بك علناً",
                    "أغلق البرنامج عند عدم الاستخدام",
                    "تحقق من الملفات المستقبلة قبل فتحها"
                ]
            },
            {
                "title": "🛠️ حل المشاكل",
                "tips": [
                    "إذا فشل الإرسال، تحقق من IP والبورت",
                    "تأكد من السماح للبرنامج في الجدار الناري",
                    "أعد تشغيل البرنامج إذا توقف الاستقبال",
                    "تحقق من اتصال الشبكة"
                ]
            },
            {
                "title": "💡 ميزات مفيدة",
                "tips": [
                    "استخدم QR Code للاتصال السريع",
                    "فعّل الوضع الليلي من شريط الحالة",
                    "راجع سجل الأحداث لمتابعة العمليات",
                    "احفظ IP المستخدمة للوصول السريع"
                ]
            }
        ]
        
        for section in sections:
            content_layout.addWidget(self.create_section(section["title"], section["tips"]))
        
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Close button
        close_btn = QPushButton(qta.icon('fa5s.check'), " فهمت!")
        close_btn.clicked.connect(self.close)
        close_btn.setObjectName("successButton")
        layout.addWidget(close_btn)
    
    def create_section(self, title, tips):
        """Create a tips section"""
        section = QFrame()
        section.setObjectName("sectionFrame")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(10)
        
        # Section title
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Tips
        for tip in tips:
            tip_layout = QHBoxLayout()
            tip_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            tip_layout.setSpacing(10)
            
            tip_label = QLabel(tip)
            tip_label.setObjectName("tipText")
            tip_label.setWordWrap(True)
            
            bullet = QLabel("•")
            bullet.setStyleSheet("color: #667eea; font-size: 16px; font-weight: bold;")
            bullet.setFixedWidth(20)
            
            tip_layout.addWidget(tip_label, 1)
            tip_layout.addWidget(bullet, 0)
            
            layout.addLayout(tip_layout)
        
        return section
    
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
                QLabel#sectionTitle {
                    color: #89b4fa;
                }
                QLabel#tipText {
                    color: #cdd6f4;
                    font-size: 12px;
                }
                QFrame#sectionFrame {
                    background: #313244;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 5px;
                }
                QScrollArea {
                    border: none;
                    background: transparent;
                }
                QPushButton#successButton {
                    background: #27ae60;
                    color: white;
                    border: none;
                    padding: 12px 30px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton#successButton:hover {
                    background: #229954;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background: white;
                    color: #2c3e50;
                }
                QLabel#sectionTitle {
                    color: #2c3e50;
                }
                QLabel#tipText {
                    color: #34495e;
                    font-size: 12px;
                }
                QFrame#sectionFrame {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 5px;
                }
                QScrollArea {
                    border: none;
                    background: transparent;
                }
                QPushButton#successButton {
                    background: #27ae60;
                    color: white;
                    border: none;
                    padding: 12px 30px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton#successButton:hover {
                    background: #229954;
                }
            """)
