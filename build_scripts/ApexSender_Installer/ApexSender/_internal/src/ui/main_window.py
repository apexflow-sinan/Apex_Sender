"""Main application window"""
import os
import sys
import threading
import socket
import subprocess
import ctypes
import qtawesome as qta
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QMessageBox, QFrame, QTextEdit, QCheckBox, QPushButton, QStatusBar, QScrollArea
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

from src.config.settings import DEFAULT_PORT, ICON_FILE, WINDOW_WIDTH, WINDOW_HEIGHT, ANIMATION_DURATION
from src.config.styles import LIGHT_STYLESHEET, DARK_STYLESHEET
from src.core.settings_manager import SettingsManager
from src.core.status_manager import StatusManager, AppStatus
from src.utils.network_utils import get_local_ip
from src.ui.sender_tab import SenderTab
from src.ui.receiver_tab import ReceiverTab
from src.ui.web_tab import WebTab
from src.ui.games_tab import GamesTab
from src.ui.qr_dialog import show_qr_dialog
from src.network.receiver import ReceiverThread

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()
        self.status_manager = StatusManager()
        self.receiver_worker = None
        self.receiver_thread = None
        self.setup_window()
        self.setup_ui()
        self.apply_theme()
        self.start_receiver()
        self.check_firewall()
        self.animate_window()
        
        # Set initial status based on active tab
        self.status_manager.set_status(AppStatus.READY_TO_SEND)
        self.log_message("التطبيق جاهز")
    
    def setup_window(self):
        """Setup window properties"""
        self.setWindowTitle("Apex Sender")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Center window on screen
        from PyQt6.QtGui import QScreen
        screen = QScreen.availableGeometry(self.screen())
        x = (screen.width() - WINDOW_WIDTH) // 2
        y = (screen.height() - WINDOW_HEIGHT) // 2
        self.move(x, y)
        
        if os.path.exists(ICON_FILE):
            self.setWindowIcon(QIcon(ICON_FILE))
    
    def setup_ui(self):
        """Setup user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Title bar
        main_layout.addWidget(self.create_title_bar())
        
        # Tabs (fixed at top)
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        self.tabs = tabs
        
        # Create tab widgets
        sender_widget = SenderTab(self.settings_manager, self.status_manager, self.log_message)
        receiver_widget = ReceiverTab(self.settings_manager, self.status_manager, self.log_message)
        web_widget = WebTab(self.settings_manager, self.log_message)
        games_widget = GamesTab(self.settings_manager, self.log_message)
        
        # Store original widgets for access
        self.sender_tab = sender_widget
        self.receiver_tab = receiver_widget
        self.web_tab = web_widget
        self.games_tab = games_widget
        
        # Add tabs with scroll areas
        tabs.addTab(self.create_scrollable_tab(sender_widget), qta.icon('fa5s.upload'), "إرسال")
        tabs.addTab(self.create_scrollable_tab(receiver_widget), qta.icon('fa5s.download'), "استقبال")
        tabs.addTab(self.create_scrollable_tab(web_widget), qta.icon('fa5s.globe'), "Web")
        tabs.addTab(self.create_scrollable_tab(games_widget), qta.icon('fa5s.gamepad'), "ألعاب ويب")
        tabs.currentChanged.connect(self.on_tab_changed)
        
        main_layout.addWidget(tabs)
        
        # Log section
        main_layout.addWidget(self.create_log_section())
        
        # Status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create beautiful menu bar"""
        self.menubar = self.menuBar()
        self.update_menu_style()
        
        # Menu
        self.main_menu = self.menubar.addMenu("☰ القائمة")
        
        # Advanced settings
        advanced_action = self.main_menu.addAction(qta.icon('fa5s.cog', color='#667eea'), " إعدادات متقدمة")
        advanced_action.triggered.connect(self.show_advanced_settings)
        
        self.main_menu.addSeparator()
        
        # Help
        help_action = self.main_menu.addAction(qta.icon('fa5s.question-circle', color='#3498db'), " التعليمات والنصائح")
        help_action.triggered.connect(self.show_help)
        
        # About
        about_action = self.main_menu.addAction(qta.icon('fa5s.info-circle', color='#27ae60'), " حول البرنامج")
        about_action.triggered.connect(self.show_about)
        
        self.main_menu.addSeparator()
        
        # Exit
        exit_action = self.main_menu.addAction(qta.icon('fa5s.sign-out-alt', color='#e74c3c'), " خروج")
        exit_action.triggered.connect(self.close)
    
    def update_menu_style(self):
        """Update menu style based on theme"""
        is_dark = self.settings_manager.get("dark_mode", False)
        
        if is_dark:
            self.menubar.setStyleSheet("""
                QMenuBar {
                    background: #1e1e2e;
                    border: none;
                    font-size: 13px;
                    color: #cdd6f4;
                }
                QMenuBar::item {
                    padding: 8px 15px;
                    border-radius: 5px;
                    background: transparent;
                }
                QMenuBar::item:selected {
                    background: rgba(102, 126, 234, 0.2);
                }
                QMenu {
                    background: #313244;
                    border: 1px solid #45475a;
                    border-radius: 8px;
                    padding: 5px;
                    color: #cdd6f4;
                }
                QMenu::item {
                    padding: 10px 35px 10px 25px;
                    border-radius: 5px;
                }
                QMenu::item:selected {
                    background: #667eea;
                    color: white;
                }
                QMenu::separator {
                    height: 1px;
                    background: #45475a;
                    margin: 5px 10px;
                }
            """)
        else:
            self.menubar.setStyleSheet("""
                QMenuBar {
                    background: transparent;
                    border: none;
                    font-size: 13px;
                }
                QMenuBar::item {
                    padding: 8px 15px;
                    border-radius: 5px;
                }
                QMenuBar::item:selected {
                    background: rgba(102, 126, 234, 0.1);
                }
                QMenu {
                    background: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 5px;
                }
                QMenu::item {
                    padding: 10px 35px 10px 25px;
                    border-radius: 5px;
                }
                QMenu::item:selected {
                    background: #667eea;
                    color: white;
                }
                QMenu::separator {
                    height: 1px;
                    background: #e0e0e0;
                    margin: 5px 10px;
                }
            """)
    
    def show_advanced_settings(self):
        """Show advanced settings dialog"""
        from src.ui.setup_dialog import SetupDialog
        dialog = SetupDialog(self)
        dialog.exec()
    
    def show_help(self):
        """Show help dialog"""
        from src.ui.help_dialog import HelpDialog
        dialog = HelpDialog(self)
        dialog.exec()
    
    def show_about(self):
        """Show about dialog"""
        from src.ui.about_dialog import AboutDialog
        dialog = AboutDialog(self)
        dialog.exec()
    
    def create_scrollable_tab(self, tab_widget):
        """Wrap tab content in scroll area"""
        scroll_area = QScrollArea()
        scroll_area.setWidget(tab_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        return scroll_area
    
    def create_title_bar(self):
        """Create title bar widget"""
        title_bar = QWidget(objectName="TitleBar")
        layout = QVBoxLayout(title_bar)
        
        # Title
        title_hbox = QHBoxLayout()
        title_hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_hbox.addWidget(QLabel(pixmap=qta.icon('fa5s.rocket', color='white').pixmap(28, 28)))
        title_hbox.addWidget(QLabel("Apex Sender", objectName="TitleLabel"))
        
        # IP
        ip_hbox = QHBoxLayout()
        ip_hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ip_hbox.addWidget(QLabel(pixmap=qta.icon('fa5s.globe', color='#1abc9c').pixmap(16, 16)))
        ip_hbox.addWidget(QLabel(f"IP: {get_local_ip()}", objectName="IPLabel"))
        
        layout.addLayout(title_hbox)
        layout.addLayout(ip_hbox)
        
        return title_bar
    
    def create_log_section(self):
        """Create collapsible log section widget"""
        # Log content (hidden by default)
        self.log_edit = QTextEdit(readOnly=True)
        self.log_edit.setMaximumHeight(150)
        self.log_edit.setMinimumHeight(150)
        self.log_edit.setVisible(False)
        self.log_edit.setObjectName("logEdit")
        
        return self.log_edit
    
    def update_log_icon(self):
        """Update log icon based on visibility"""
        is_visible = self.log_edit.isVisible()
        icon_name = 'fa5s.folder-open' if is_visible else 'fa5s.folder'
        color = '#3498db'
        tooltip = "إغلاق سجل الأحداث" if is_visible else "فتح سجل الأحداث"
        self.log_toggle_icon.setIcon(qta.icon(icon_name, color=color))
        self.log_toggle_icon.setToolTip(tooltip)
    
    def update_status_bar(self, message: str, icon: str, color: str):
        """Update status bar with new status"""
        self.status_icon.setPixmap(qta.icon(icon, color=color).pixmap(16, 16))
        self.status_text.setText(message)
        self.status_text.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def on_tab_changed(self, index: int):
        """Handle tab change"""
        if not self.status_manager.is_busy():
            if index == 0:  # Sender tab
                self.status_manager.set_status(AppStatus.READY_TO_SEND)
            else:  # Receiver tab
                self.status_manager.set_status(AppStatus.READY_TO_RECEIVE)
    
    def toggle_log(self):
        """Toggle log visibility"""
        is_visible = self.log_edit.isVisible()
        self.log_edit.setVisible(not is_visible)
        self.update_log_icon()
    
    def log_message(self, msg):
        """Add message to log"""
        import time
        self.log_edit.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    
    def apply_theme(self):
        """Apply current theme"""
        is_dark = self.settings_manager.get("dark_mode", False)
        self.setStyleSheet(DARK_STYLESHEET if is_dark else LIGHT_STYLESHEET)
    
    def create_status_bar(self):
        """Create status bar with Log, QR and Dark Mode"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # Status indicator
        self.status_icon = QLabel()
        self.status_text = QLabel()
        status_bar.addWidget(self.status_icon)
        status_bar.addWidget(self.status_text)
        
        # Connect status manager
        self.status_manager.status_changed.connect(self.update_status_bar)
        
        status_bar.addPermanentWidget(QLabel("  "))  # Spacer
        
        # Log toggle button
        self.log_toggle_icon = QPushButton()
        self.log_toggle_icon.setFlat(True)
        self.log_toggle_icon.setToolTip("فتح سجل الأحداث")
        self.log_toggle_icon.clicked.connect(self.toggle_log)
        self.update_log_icon()
        status_bar.addPermanentWidget(self.log_toggle_icon)
        
        # QR Code button
        qr_btn = QPushButton()
        qr_btn.setFlat(True)
        qr_btn.setIcon(qta.icon('fa5s.qrcode', color='#1abc9c'))
        qr_btn.setToolTip("Show QR Code")
        qr_btn.clicked.connect(lambda: show_qr_dialog(self, get_local_ip(), DEFAULT_PORT))
        status_bar.addPermanentWidget(qr_btn)
        
        # Dark mode toggle
        self.dark_mode_icon = QPushButton()
        self.dark_mode_icon.setFlat(True)
        self.dark_mode_icon.setToolTip("Toggle Dark Mode")
        self.dark_mode_icon.clicked.connect(self.toggle_dark_mode)
        self.update_dark_mode_icon()
        status_bar.addPermanentWidget(self.dark_mode_icon)
    
    def update_dark_mode_icon(self):
        """Update dark mode icon based on current theme"""
        is_dark = self.settings_manager.get("dark_mode", False)
        icon_name = 'fa5s.moon' if not is_dark else 'fa5s.sun'
        color = '#f39c12' if not is_dark else '#f1c40f'
        self.dark_mode_icon.setIcon(qta.icon(icon_name, color=color))
    
    def toggle_dark_mode(self):
        """Toggle dark mode"""
        is_dark = self.settings_manager.get("dark_mode", False)
        self.settings_manager.set("dark_mode", not is_dark)
        self.apply_theme()
        self.update_dark_mode_icon()
        self.update_menu_style()
    
    def animate_window(self):
        """Animate window appearance"""
        animation = QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(ANIMATION_DURATION)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        self.animation = animation
    
    def start_receiver(self):
        """Start receiver thread"""
        save_dir = self.settings_manager.get("save_directory")
        
        # Try to create directory, fallback to default if permission denied
        try:
            os.makedirs(save_dir, exist_ok=True)
        except (PermissionError, OSError):
            from src.config.settings import DEFAULT_SAVE_DIR
            save_dir = DEFAULT_SAVE_DIR
            self.settings_manager.set("save_directory", save_dir)
            os.makedirs(save_dir, exist_ok=True)
            self.log_message(f"تم تغيير مجلد الحفظ إلى: {save_dir}")
        
        self.receiver_worker = ReceiverThread(DEFAULT_PORT, save_dir)
        self.receiver_thread = threading.Thread(target=self.receiver_worker.run, daemon=True)
        
        self.receiver_worker.signals.log_message.connect(self.log_message)
        self.receiver_worker.signals.progress_update.connect(self.receiver_tab.update_progress)
        self.receiver_worker.signals.task_finished.connect(self.receiver_tab.on_finished)
        self.receiver_worker.signals.ask_extract.connect(self.receiver_tab.ask_extract)
        self.receiver_worker.signals.file_received.connect(self.receiver_tab.add_received_file)
        
        self.receiver_thread.start()
    
    def check_firewall(self):
        """Check and setup firewall rules"""
        if os.name != 'nt' or '--skip-firewall' in sys.argv:
            return
        
        try:
            rule_name = f'ApexSenderPort{DEFAULT_PORT}'
            result = subprocess.run(
                ['netsh', 'advfirewall', 'firewall', 'show', 'rule', f'name={rule_name}'],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if 'No rules match' in result.stdout:
                reply = QMessageBox.question(
                    self, "Firewall Setup",
                    "Allow Apex Sender through Windows Firewall?"
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.setup_firewall_rules()
        except Exception as e:
            self.log_message(f"Firewall check failed: {e}")
    
    def setup_firewall_rules(self):
        """Setup firewall rules"""
        try:
            rule_name = f'ApexSenderPort{DEFAULT_PORT}'
            port = str(DEFAULT_PORT)
            
            cmds = [
                ['netsh', 'advfirewall', 'firewall', 'add', 'rule', f'name={rule_name}',
                 'dir=in', 'action=allow', 'protocol=TCP', f'localport={port}'],
                ['netsh', 'advfirewall', 'firewall', 'add', 'rule', f'name={rule_name} OUT',
                 'dir=out', 'action=allow', 'protocol=TCP', f'localport={port}']
            ]
            
            for cmd in cmds:
                subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            QMessageBox.information(self, "Success", "Firewall configured successfully!")
            self.log_message(f"Firewall configured - Port {DEFAULT_PORT} opened")
        
        except subprocess.CalledProcessError:
            reply = QMessageBox.question(
                self, "Admin Required",
                "Firewall setup requires administrator privileges.\n\nRestart as administrator?"
            )
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    args = [arg for arg in sys.argv if arg != '--skip-firewall'] + ['--skip-firewall']
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(args), None, 1)
                    sys.exit(0)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to restart: {e}")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Firewall setup failed: {e}")
    
    def closeEvent(self, event):
        """Handle window close event"""
        try:
            # Cleanup sender tab
            if hasattr(self, 'sender_tab'):
                self.sender_tab.cleanup()
            
            # Cleanup receiver tab timers
            if hasattr(self, 'receiver_tab'):
                self.receiver_tab.cleanup()
            
            # Cleanup games tab
            if hasattr(self, 'games_tab'):
                self.games_tab.cleanup()
            
            # Stop receiver worker
            if hasattr(self, 'receiver_worker') and self.receiver_worker:
                self.receiver_worker.stop()
            
            # Send dummy connection to stop server
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect(('127.0.0.1', DEFAULT_PORT))
            except:
                pass
            
            # Wait for thread to finish
            if hasattr(self, 'receiver_thread') and self.receiver_thread and self.receiver_thread.is_alive():
                self.receiver_thread.join(timeout=2)
        
        except Exception as e:
            print(f"Error during close: {e}")
        finally:
            event.accept()
