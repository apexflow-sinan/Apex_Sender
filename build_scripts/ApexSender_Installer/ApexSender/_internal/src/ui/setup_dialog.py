from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QPushButton, QLabel, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import qtawesome as qta
from src.core.firewall_helper import FirewallHelper
from src.core.config_manager import ConfigManager
from src.core.settings_manager import SettingsManager
from src.core.platform_manager import PlatformManager
from src.utils.network_utils import get_local_ip
from src.widgets.loading_indicator import LoadingIndicator

class SetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager()
        self.settings_manager = SettingsManager()
        self.loading = LoadingIndicator(self)
        self.init_ui()
        QTimer.singleShot(100, self.load_settings)
        self.apply_theme()
    
    def init_ui(self):
        platform = PlatformManager.get_platform()
        platform_name = "Windows" if platform == "windows" else "Linux" if platform == "linux" else "macOS"
        
        self.setWindowTitle(f"⚙️ إعدادات متقدمة - {platform_name}")
        self.setMinimumWidth(550)
        self.setMinimumHeight(500)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel(f"🚨 إعدادات {platform_name}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setObjectName("headerLabel")
        layout.addWidget(header)
        
        layout.addWidget(self.create_firewall_group())
        layout.addWidget(self.create_service_group())
        layout.addWidget(self.create_network_info_group())
        
        layout.addStretch()
        layout.addLayout(self.create_buttons())
        
        self.setLayout(layout)
    
    def create_firewall_group(self):
        group = QGroupBox("🔥 جدار الحماية")
        group.setObjectName("settingsGroup")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        self.firewall_status_label = QLabel()
        self.firewall_status_label.setWordWrap(True)
        layout.addWidget(self.firewall_status_label)
        
        btn_layout = QHBoxLayout()
        
        self.check_firewall_btn = QPushButton(qta.icon('fa5s.search'), " فحص الحالة")
        self.check_firewall_btn.clicked.connect(self.check_firewall)
        self.check_firewall_btn.setObjectName("actionButton")
        btn_layout.addWidget(self.check_firewall_btn)
        
        self.add_firewall_btn = QPushButton(qta.icon('fa5s.shield-alt'), " إضافة استثناء")
        self.add_firewall_btn.clicked.connect(self.add_firewall_rules)
        self.add_firewall_btn.setObjectName("actionButton")
        btn_layout.addWidget(self.add_firewall_btn)
        
        layout.addLayout(btn_layout)
        group.setLayout(layout)
        return group
    
    def create_service_group(self):
        platform = PlatformManager.get_platform()
        
        # Platform-specific titles
        if platform == "windows":
            title = "🚀 التشغيل التلقائي (Windows Service)"
        elif platform == "linux":
            title = "🚀 التشغيل التلقائي (Systemd Service)"
        else:
            title = "🚀 التشغيل التلقائي (Launch Daemon)"
        
        group = QGroupBox(title)
        group.setObjectName("settingsGroup")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        self.service_status_label = QLabel()
        self.service_status_label.setWordWrap(True)
        layout.addWidget(self.service_status_label)
        
        self.run_as_service_cb = QCheckBox(" تشغيل السيرفر في الخلفية")
        layout.addWidget(self.run_as_service_cb)
        
        self.auto_start_cb = QCheckBox(" بدء مع النظام")
        layout.addWidget(self.auto_start_cb)
        
        btn_layout = QHBoxLayout()
        
        self.install_service_btn = QPushButton(qta.icon('fa5s.download'), " تثبيت الخدمة")
        self.install_service_btn.clicked.connect(self.install_service)
        self.install_service_btn.setObjectName("actionButton")
        btn_layout.addWidget(self.install_service_btn)
        
        self.uninstall_service_btn = QPushButton(qta.icon('fa5s.trash'), " إلغاء التثبيت")
        self.uninstall_service_btn.clicked.connect(self.uninstall_service)
        self.uninstall_service_btn.setObjectName("actionButton")
        btn_layout.addWidget(self.uninstall_service_btn)
        
        layout.addLayout(btn_layout)
        group.setLayout(layout)
        return group
    
    def create_network_info_group(self):
        group = QGroupBox("📋 معلومات الشبكة")
        group.setObjectName("settingsGroup")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        ip = get_local_ip()
        web_port = self.config.get('web_port', 8080)
        network_port = self.config.get('network_port', 9999)
        
        # IP info
        ip_layout = QHBoxLayout()
        ip_icon = QLabel()
        ip_icon.setPixmap(qta.icon('fa5s.network-wired', color='#3498db').pixmap(16, 16))
        ip_label = QLabel(f"عنوان IP: {ip}")
        ip_label.setFont(QFont("Arial", 10))
        ip_layout.addWidget(ip_icon)
        ip_layout.addWidget(ip_label)
        ip_layout.addStretch()
        layout.addLayout(ip_layout)
        
        # Ports info
        ports_layout = QHBoxLayout()
        ports_icon = QLabel()
        ports_icon.setPixmap(qta.icon('fa5s.plug', color='#e74c3c').pixmap(16, 16))
        ports_label = QLabel(f"المنافذ: Web ({web_port}), Network ({network_port})")
        ports_label.setFont(QFont("Arial", 10))
        ports_layout.addWidget(ports_icon)
        ports_layout.addWidget(ports_label)
        ports_layout.addStretch()
        layout.addLayout(ports_layout)
        
        group.setLayout(layout)
        return group
    
    def create_buttons(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        cancel_btn = QPushButton(qta.icon('fa5s.times'), " إلغاء")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setObjectName("cancelButton")
        layout.addWidget(cancel_btn)
        
        apply_btn = QPushButton(qta.icon('fa5s.check'), " تطبيق")
        apply_btn.clicked.connect(self.apply_settings)
        apply_btn.setObjectName("applyButton")
        layout.addWidget(apply_btn)
        
        save_btn = QPushButton(qta.icon('fa5s.save'), " حفظ")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setObjectName("saveButton")
        layout.addWidget(save_btn)
        
        return layout
    
    def load_settings(self):
        try:
            self.run_as_service_cb.setChecked(self.config.get('run_as_service', False))
            self.auto_start_cb.setChecked(self.config.get('auto_start', False))
            self.check_firewall()
            self.update_service_status()
        except Exception as e:
            print(f"Warning loading settings: {e}")
    
    def check_firewall(self):
        self.loading.show_indicator()
        QTimer.singleShot(50, self._do_check_firewall)
    
    def _do_check_firewall(self):
        try:
            ports = [self.config.get('web_port', 8080), self.config.get('network_port', 9999)]
            results = FirewallHelper.check_all_ports(ports)
            
            all_configured = all(results.values())
            
            if all_configured:
                self.firewall_status_label.setText("✅ جدار الحماية مُعد بشكل صحيح")
                self.firewall_status_label.setStyleSheet("color: green;")
            else:
                missing = [str(p) for p, configured in results.items() if not configured]
                self.firewall_status_label.setText(f"⚠️ المنافذ التالية تحتاج إعداد: {', '.join(missing)}")
                self.firewall_status_label.setStyleSheet("color: orange;")
        finally:
            self.loading.hide_indicator()
    
    def add_firewall_rules(self):
        platform = PlatformManager.get_platform()
        
        if not FirewallHelper.is_admin():
            if platform == "windows":
                msg = "يجب تشغيل البرنامج كمسؤول (Administrator) لإضافة قواعد جدار الحماية"
            else:
                msg = "يجب تشغيل البرنامج بصلاحيات الجذر (sudo) لإضافة قواعد جدار الحماية"
            QMessageBox.warning(self, "تحذير", msg)
            return
        
        self.loading.show_indicator()
        QTimer.singleShot(50, self._do_add_firewall)
    
    def _do_add_firewall(self):
        try:
            ports = [self.config.get('web_port', 8080), self.config.get('network_port', 9999)]
            success, results = FirewallHelper.add_all_rules(ports)
            
            if success:
                QMessageBox.information(self, "نجح", "تم إضافة قواعد جدار الحماية بنجاح")
                self.config.set('firewall_configured', True)
            else:
                QMessageBox.warning(self, "خطأ", "فشل في إضافة بعض القواعد")
            
            self.check_firewall()
        finally:
            self.loading.hide_indicator()
    
    def update_service_status(self):
        try:
            platform = PlatformManager.get_platform()
            
            # Check if web server is running (check port 8080)
            import socket
            web_port = self.config.get('web_port', 8080)
            
            def is_port_in_use(port):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        return s.connect_ex(('localhost', port)) == 0
                except:
                    return False
            
            server_running = is_port_in_use(web_port)
            
            if server_running:
                self.service_status_label.setText("✅ السيرفر يعمل")
                self.service_status_label.setStyleSheet("color: green;")
                return
            
            # Check service status based on platform
            try:
                from src.service.cross_platform_service import CrossPlatformService
                service = CrossPlatformService()
                status = service.get_status()
                
                if status == "running":
                    service_type = "Windows Service" if platform == "windows" else "Systemd Service" if platform == "linux" else "Launch Daemon"
                    self.service_status_label.setText(f"✅ الخدمة تعمل ({service_type})")
                    self.service_status_label.setStyleSheet("color: green;")
                    self.install_service_btn.setEnabled(False)
                    self.uninstall_service_btn.setEnabled(True)
                    return
                elif status == "stopped":
                    self.service_status_label.setText("⏸️ الخدمة متوقفة")
                    self.service_status_label.setStyleSheet("color: orange;")
                    self.install_service_btn.setEnabled(False)
                    self.uninstall_service_btn.setEnabled(True)
                    return
                elif status == "not_installed":
                    self.service_status_label.setText("❌ السيرفر متوقف (الخدمة غير مثبتة)")
                    self.service_status_label.setStyleSheet("color: red;")
                    self.install_service_btn.setEnabled(True)
                    self.uninstall_service_btn.setEnabled(False)
                    return
            except ImportError:
                self.service_status_label.setText("⚠️ خدمة الخلفية غير متوفرة")
                self.service_status_label.setStyleSheet("color: orange;")
                self.install_service_btn.setEnabled(False)
                self.uninstall_service_btn.setEnabled(False)
                return
            
            self.service_status_label.setText("❌ السيرفر متوقف")
            self.service_status_label.setStyleSheet("color: red;")
            self.install_service_btn.setEnabled(True)
            self.uninstall_service_btn.setEnabled(False)
        except Exception as e:
            self.service_status_label.setText(f"⚠️ خطأ: {str(e)[:50]}")
            self.service_status_label.setStyleSheet("color: orange;")
            self.install_service_btn.setEnabled(False)
            self.uninstall_service_btn.setEnabled(False)
    
    def install_service(self):
        try:
            platform = PlatformManager.get_platform()
            
            if not FirewallHelper.is_admin():
                if platform == "windows":
                    msg = "يجب تشغيل البرنامج كمسؤول (Administrator) لتثبيت الخدمة"
                else:
                    msg = "يجب تشغيل البرنامج بصلاحيات الجذر (sudo) لتثبيت الخدمة"
                QMessageBox.warning(self, "تحذير", msg)
                return
            
            self.loading.show_indicator()
            QTimer.singleShot(50, self._do_install_service)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ: {str(e)}")
    
    def _do_install_service(self):
        try:
            from src.service.cross_platform_service import CrossPlatformService
            service = CrossPlatformService()
            success, msg = service.install()
            
            if success:
                QMessageBox.information(self, "نجح", msg)
            else:
                QMessageBox.warning(self, "خطأ", msg)
            
            self.update_service_status()
        except ImportError:
            QMessageBox.warning(self, "خطأ", "خدمة الخلفية غير متوفرة في هذا الإصدار")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل تثبيت الخدمة:\n{str(e)}")
        finally:
            self.loading.hide_indicator()
    
    def uninstall_service(self):
        try:
            platform = PlatformManager.get_platform()
            
            if not FirewallHelper.is_admin():
                if platform == "windows":
                    msg = "يجب تشغيل البرنامج كمسؤول (Administrator) لإلغاء تثبيت الخدمة"
                else:
                    msg = "يجب تشغيل البرنامج بصلاحيات الجذر (sudo) لإلغاء تثبيت الخدمة"
                QMessageBox.warning(self, "تحذير", msg)
                return
            
            reply = QMessageBox.question(self, "تأكيد", "هل تريد إلغاء تثبيت الخدمة؟",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                self.loading.show_indicator()
                QTimer.singleShot(50, self._do_uninstall_service)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ: {str(e)}")
    
    def _do_uninstall_service(self):
        try:
            from src.service.cross_platform_service import CrossPlatformService
            service = CrossPlatformService()
            success, msg = service.uninstall()
            
            if success:
                QMessageBox.information(self, "نجح", msg)
            else:
                QMessageBox.warning(self, "خطأ", msg)
            
            self.update_service_status()
        except ImportError:
            QMessageBox.warning(self, "خطأ", "خدمة الخلفية غير متوفرة في هذا الإصدار")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل إلغاء تثبيت الخدمة:\n{str(e)}")
        finally:
            self.loading.hide_indicator()
    
    def save_settings(self):
        self.apply_settings()
        self.accept()
    
    def apply_settings(self):
        try:
            self.config.set('run_as_service', self.run_as_service_cb.isChecked())
            self.config.set('auto_start', self.auto_start_cb.isChecked())
            
            try:
                from src.service.cross_platform_service import CrossPlatformService
                service = CrossPlatformService()
                
                if self.auto_start_cb.isChecked() and service.is_installed():
                    platform = PlatformManager.get_platform()
                    if platform == "windows":
                        try:
                            from src.service.service_installer import ServiceInstaller
                            ServiceInstaller.set_auto_start(True)
                        except ImportError:
                            pass
            except ImportError:
                pass
            
            QMessageBox.information(self, "نجح", "تم حفظ الإعدادات بنجاح")
        except Exception as e:
            QMessageBox.warning(self, "تحذير", f"تم حفظ الإعدادات مع بعض التحذيرات:\n{str(e)}")
    
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
                QLabel#headerLabel {
                    color: #667eea;
                }
                QGroupBox {
                    font-weight: bold;
                    font-size: 13px;
                    border: 2px solid #45475a;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                    color: #cdd6f4;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QCheckBox {
                    color: #cdd6f4;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 4px;
                    border: 2px solid #45475a;
                    background: #313244;
                }
                QCheckBox::indicator:checked {
                    background: #667eea;
                    border-color: #667eea;
                }
                QPushButton#actionButton {
                    background: #313244;
                    color: #cdd6f4;
                    border: 1px solid #45475a;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-size: 12px;
                }
                QPushButton#actionButton:hover {
                    background: #45475a;
                    border-color: #667eea;
                }
                QPushButton#saveButton {
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 10px 25px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#saveButton:hover {
                    background: #5568d3;
                }
                QPushButton#applyButton {
                    background: #27ae60;
                    color: white;
                    border: none;
                    padding: 10px 25px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#applyButton:hover {
                    background: #229954;
                }
                QPushButton#cancelButton {
                    background: #45475a;
                    color: #cdd6f4;
                    border: none;
                    padding: 10px 25px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#cancelButton:hover {
                    background: #585b70;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background: white;
                    color: #2c3e50;
                }
                QLabel#headerLabel {
                    color: #667eea;
                }
                QGroupBox {
                    font-weight: bold;
                    font-size: 13px;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                    color: #2c3e50;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QCheckBox {
                    color: #2c3e50;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 4px;
                    border: 2px solid #bdc3c7;
                    background: white;
                }
                QCheckBox::indicator:checked {
                    background: #667eea;
                    border-color: #667eea;
                }
                QPushButton#actionButton {
                    background: #f8f9fa;
                    color: #2c3e50;
                    border: 1px solid #dee2e6;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-size: 12px;
                }
                QPushButton#actionButton:hover {
                    background: #e9ecef;
                    border-color: #667eea;
                }
                QPushButton#saveButton {
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 10px 25px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#saveButton:hover {
                    background: #5568d3;
                }
                QPushButton#applyButton {
                    background: #27ae60;
                    color: white;
                    border: none;
                    padding: 10px 25px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#applyButton:hover {
                    background: #229954;
                }
                QPushButton#cancelButton {
                    background: #95a5a6;
                    color: white;
                    border: none;
                    padding: 10px 25px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton#cancelButton:hover {
                    background: #7f8c8d;
                }
            """)
