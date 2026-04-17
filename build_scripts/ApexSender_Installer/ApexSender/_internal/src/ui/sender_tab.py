"""Sender tab widget"""
import threading
import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QProgressBar, QFrame, QFileDialog, QMessageBox, QComboBox, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSlot

from src.config.settings import DEFAULT_PORT
from src.core.status_manager import AppStatus
from src.utils.network_utils import get_local_ip, check_connection
from src.utils.file_utils import compress_folder
from src.utils.sound_utils import play_success_sound, play_error_sound
from src.utils.file_dialog_utils import get_open_filename, get_open_filenames, get_existing_directory
from src.network.sender import SenderThread

class SenderTab(QWidget):
    """Sender tab widget"""
    
    def __init__(self, settings_manager, status_manager, log_callback):
        super().__init__()
        self.settings_manager = settings_manager
        self.status_manager = status_manager
        self.log_callback = log_callback
        self.sender_thread = None
        self.sender_worker = None
        self.is_sending = False  # حماية من الإرسال المتكرر
        self.setObjectName("TabContent")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        
        # IP input card
        card = QFrame(objectName="card")
        card.setMaximumWidth(500)
        card_layout = QVBoxLayout(card)
        
        LABEL_W = 90
        
        # IP input row
        ip_row = QHBoxLayout()
        ip_icon = QLabel()
        ip_icon.setPixmap(qta.icon('fa5s.map-marker-alt').pixmap(16, 16))
        ip_icon.setFixedWidth(20)
        ip_row.addWidget(ip_icon)
        ip_label = QLabel("العنوان:")
        ip_label.setFixedWidth(LABEL_W)
        ip_row.addWidget(ip_label)
        
        ip_parts = get_local_ip().split('.')
        self.ip_boxes = []
        for i in range(4):
            box = QLineEdit()
            box.setFixedWidth(55)
            box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.setMaxLength(3)
            if i < 3:
                box.setText(ip_parts[i] if i < len(ip_parts) else "")
            else:
                box.setPlaceholderText("?")
            box.textChanged.connect(self.check_ip_complete)
            self.ip_boxes.append(box)
            ip_row.addWidget(box)
            if i < 3:
                dot = QLabel(".")
                dot.setFixedWidth(10)
                dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
                ip_row.addWidget(dot)
        ip_row.addStretch()
        card_layout.addLayout(ip_row)
        
        # IP history row
        hist_row = QHBoxLayout()
        hist_icon = QLabel()
        hist_icon.setPixmap(qta.icon('fa5s.history').pixmap(16, 16))
        hist_icon.setFixedWidth(20)
        hist_row.addWidget(hist_icon)
        hist_label = QLabel("السجل:")
        hist_label.setFixedWidth(LABEL_W)
        hist_row.addWidget(hist_label)
        self.ip_combo = QComboBox()
        self.ip_combo.addItem("اختر من السجل...")
        self.ip_combo.addItems(self.settings_manager.get("ip_history", []))
        self.ip_combo.currentTextChanged.connect(self.on_ip_selected)
        hist_row.addWidget(self.ip_combo)
        card_layout.addLayout(hist_row)
        
        layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.send_file_btn = QPushButton(qta.icon('fa5s.file'), " إرسال ملف")
        self.send_file_btn.clicked.connect(self.send_file)
        self.send_file_btn.setEnabled(False)
        self.send_file_btn.setMaximumWidth(180)
        btn_layout.addWidget(self.send_file_btn)
        
        self.send_files_btn = QPushButton(qta.icon('fa5s.copy'), " ملفات متعددة")
        self.send_files_btn.clicked.connect(self.send_multiple_files)
        self.send_files_btn.setEnabled(False)
        self.send_files_btn.setMaximumWidth(180)
        btn_layout.addWidget(self.send_files_btn)
        
        self.send_folder_btn = QPushButton(qta.icon('fa5s.folder'), " إرسال مجلد")
        self.send_folder_btn.clicked.connect(self.send_folder)
        self.send_folder_btn.setEnabled(False)
        self.send_folder_btn.setMaximumWidth(180)
        btn_layout.addWidget(self.send_folder_btn)
        
        self.send_text_btn = QPushButton(qta.icon('fa5s.comment'), " إرسال نص")
        self.send_text_btn.clicked.connect(self._toggle_text_input)
        self.send_text_btn.setEnabled(False)
        self.send_text_btn.setMaximumWidth(180)
        btn_layout.addWidget(self.send_text_btn)
        
        layout.addLayout(btn_layout)
        
        # Text send section
        self.text_card = QFrame(objectName="card")
        self.text_card.setVisible(False)
        text_card_layout = QVBoxLayout(self.text_card)
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("اكتب النص هنا...")
        self.text_input.setMaximumHeight(100)
        text_card_layout.addWidget(self.text_input)
        text_btn_row = QHBoxLayout()
        send_text_now_btn = QPushButton(qta.icon('fa5s.paper-plane'), " إرسال")
        send_text_now_btn.setMaximumWidth(120)
        send_text_now_btn.clicked.connect(self._do_send_text)
        text_btn_row.addWidget(send_text_now_btn)
        close_text_btn = QPushButton(qta.icon('fa5s.times'), " إغلاق")
        close_text_btn.setObjectName("CancelButton")
        close_text_btn.setMaximumWidth(120)
        close_text_btn.clicked.connect(lambda: self.text_card.setVisible(False))
        text_btn_row.addWidget(close_text_btn)
        text_btn_row.addStretch()
        text_card_layout.addLayout(text_btn_row)
        layout.addWidget(self.text_card)
        
        # Cancel button
        self.cancel_btn = QPushButton(qta.icon('fa5s.times'), " إلغاء")
        self.cancel_btn.setObjectName("CancelButton")
        self.cancel_btn.clicked.connect(self.cancel_transfer)
        self.cancel_btn.setVisible(False)
        self.cancel_btn.setMaximumWidth(200)
        layout.addWidget(self.cancel_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("جاهز للإرسال", alignment=Qt.AlignmentFlag.AlignCenter)
        self.speed_label = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.speed_label)
        layout.addStretch()
    
    def on_network_changed(self, ip):
        """Update IP prefix when header network changes"""
        if ip:
            parts = ip.split('.')
            for i in range(3):
                if i < len(parts):
                    self.ip_boxes[i].setText(parts[i])
            self.ip_boxes[3].clear()
            self.ip_boxes[3].setFocus()
    
    def check_ip_complete(self):
        """Check if IP is complete and enable/disable buttons"""
        is_complete = all([box.text().strip() for box in self.ip_boxes])
        self.send_file_btn.setEnabled(is_complete)
        self.send_files_btn.setEnabled(is_complete)
        self.send_folder_btn.setEnabled(is_complete)
        self.send_text_btn.setEnabled(is_complete)
    
    def on_ip_selected(self, ip):
        """Handle IP selection from combo"""
        if ip and '.' in ip and ip != "اختر من السجل...":
            parts = ip.split('.')
            for i, part in enumerate(parts[:4]):
                if i < len(self.ip_boxes):
                    self.ip_boxes[i].setText(part)
            self.ip_combo.setCurrentIndex(0)
    
    def get_target_ip(self):
        """Get target IP from boxes"""
        return '.'.join([box.text().strip() for box in self.ip_boxes])
    
    def send_file(self):
        """Send single file"""
        file_path, _ = get_open_filename(self, "اختر ملف للإرسال")
        if file_path:
            self._send_files([file_path])
    
    def send_multiple_files(self):
        """Send multiple files"""
        file_paths, _ = get_open_filenames(self, "اختر ملفات للإرسال")
        if file_paths:
            self._send_files(file_paths)
    
    def send_folder(self):
        """Send folder"""
        # حماية من الإرسال المتكرر
        if self.is_sending:
            QMessageBox.warning(self, "تحذير", "يوجد عملية إرسال جارية بالفعل. الرجاء الانتظار حتى تنتهي.")
            return
        
        folder_path = get_existing_directory(self, "اختر مجلد للإرسال")
        if not folder_path:
            return
        
        # Check IP before starting compression
        if not all([box.text().strip() for box in self.ip_boxes]):
            QMessageBox.warning(self, "إدخال ناقص", "الرجاء إدخال عنوان IP كامل")
            return
        
        self.is_sending = True  # تفعيل الحماية
        self.status_manager.set_status(AppStatus.COMPRESSING)
        self.progress_label.setText("جاري ضغط المجلد...")
        self.progress_bar.setValue(0)
        self.set_buttons_enabled(False)
        self._activate_sender_tab()
        
        # Use QTimer to run compression in background without blocking UI
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self._compress_and_send(folder_path))
    
    def _compress_and_send(self, folder_path):
        """Compress and send folder (runs in main thread via QTimer)"""
        def progress_callback(progress, text):
            from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
            QMetaObject.invokeMethod(self, "_on_compress_progress",
                                    Qt.ConnectionType.QueuedConnection,
                                    Q_ARG(int, progress),
                                    Q_ARG(str, text))
        
        def compress_in_thread():
            try:
                zip_path = compress_folder(folder_path, progress_callback)
                # Use invokeMethod to safely update UI from thread
                from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
                QMetaObject.invokeMethod(self, "_on_compress_complete",
                                        Qt.ConnectionType.QueuedConnection,
                                        Q_ARG(str, zip_path))
            except Exception as e:
                QMetaObject.invokeMethod(self, "_on_compress_error",
                                        Qt.ConnectionType.QueuedConnection,
                                        Q_ARG(str, str(e)))
        
        threading.Thread(target=compress_in_thread, daemon=True).start()
    
    @pyqtSlot(int, str)
    def _on_compress_progress(self, progress: int, text: str):
        """Handle compression progress (called in main thread)"""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(text)
    
    @pyqtSlot(str)
    def _on_compress_complete(self, zip_path: str):
        """Handle compression complete (called in main thread)"""
        self.progress_bar.setValue(100)
        self.progress_label.setText("تم ضغط المجلد، جاري الإرسال...")
        self.log_callback(f"تم ضغط المجلد")
        self.is_sending = False  # إعادة تعيين قبل الإرسال
        self._send_files_internal([zip_path], is_temp=True)
    
    @pyqtSlot(str)
    def _on_compress_error(self, error: str):
        """Handle compression error (called in main thread)"""
        self.is_sending = False  # إلغاء الحماية عند الفشل
        self.progress_label.setText("فشل الضغط")
        self.set_buttons_enabled(True)
        self.status_manager.set_status(AppStatus.READY_TO_SEND)
        self.log_callback(f"خطأ: فشل ضغط المجلد: {error}")
        QMessageBox.critical(self, "خطأ", f"فشل ضغط المجلد:\n{error}")
    
    def _send_files(self, file_paths, is_temp=False):
        """Send files (called from main thread)"""
        # حماية من الإرسال المتكرر
        if self.is_sending:
            QMessageBox.warning(self, "تحذير", "يوجد عملية إرسال جارية بالفعل. الرجاء الانتظار حتى تنتهي.")
            return
        
        if not all([box.text().strip() for box in self.ip_boxes]):
            QMessageBox.warning(self, "إدخال ناقص", "الرجاء إدخال عنوان IP كامل")
            return
        
        self._send_files_internal(file_paths, is_temp)
    
    def _send_files_internal(self, file_paths, is_temp=False):
        """Internal send files (can be called from any thread)"""
        # حماية من الإرسال المتكرر
        if self.is_sending:
            self.log_callback("تحذير: يوجد عملية إرسال جارية بالفعل")
            return
        
        ip = self.get_target_ip()
        
        self.is_sending = True  # تفعيل الحماية
        self._activate_sender_tab()
        self.status_manager.set_status(AppStatus.SENDING)
        self.progress_bar.setValue(0)
        self.progress_label.setText("جاري الإرسال...")
        self.set_buttons_enabled(False)
        self.cancel_btn.setVisible(True)
        self.log_callback(f"إرسال إلى {ip}:{DEFAULT_PORT}...")
        
        self.sender_worker = SenderThread(ip, DEFAULT_PORT, file_paths)
        self.sender_worker.signals.log_message.connect(self.log_callback)
        self.sender_worker.signals.progress_update.connect(self.update_progress)
        self.sender_worker.signals.task_finished.connect(lambda msg: self._handle_finished(msg, ip, file_paths if is_temp else None))
        
        self.sender_thread = threading.Thread(target=self.sender_worker.run, daemon=True)
        self.sender_thread.start()
    
    def update_progress(self, value, text, speed):
        """Update progress"""
        self.progress_bar.setValue(value)
        self.progress_label.setText(text)
        self.speed_label.setText(f"السرعة: {speed:.2f} MB/s")
    
    def _handle_finished(self, message, ip, temp_files=None):
        """Handle transfer finished (called from worker thread)"""
        # Clean up temp files first
        if temp_files:
            import os
            for f in temp_files:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except:
                    pass
        
        # Update UI in main thread using invokeMethod
        from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
        QMetaObject.invokeMethod(self, "on_finished",
                                Qt.ConnectionType.QueuedConnection,
                                Q_ARG(str, message),
                                Q_ARG(str, ip))
    
    @pyqtSlot(str, str)
    def on_finished(self, message: str, ip: str):
        """Handle transfer finished (called in main thread)"""
        self.is_sending = False  # إلغاء الحماية بعد انتهاء الإرسال
        self.progress_label.setText(message)
        self.speed_label.setText("")
        self.set_buttons_enabled(True)
        self.cancel_btn.setVisible(False)
        
        if "بنجاح" in message:
            self.status_manager.set_status(AppStatus.SUCCESS)
            self.settings_manager.add_ip_to_history(ip)
            self.ip_combo.clear()
            self.ip_combo.addItem("اختر من السجل...")
            self.ip_combo.addItems(self.settings_manager.get("ip_history", []))
            play_success_sound()
            self._show_notification(f"✅ تم إرسال الملفات بنجاح إلى {ip}")
            self.status_manager.set_status(AppStatus.READY_TO_SEND)
        else:
            self.status_manager.set_status(AppStatus.ERROR)
            play_error_sound()
            QMessageBox.critical(self, "❌ خطأ", message)
            self.status_manager.set_status(AppStatus.READY_TO_SEND)
    
    def cancel_transfer(self):
        """Cancel transfer"""
        if self.sender_worker:
            self.status_manager.set_status(AppStatus.CANCELLING)
            self.sender_worker.cancel()
            self.is_sending = False  # إلغاء الحماية عند الإلغاء
            self.log_callback("إلغاء الإرسال...")
    
    def set_buttons_enabled(self, enabled):
        """Enable/disable buttons"""
        if enabled:
            self.check_ip_complete()
        else:
            self.send_file_btn.setEnabled(False)
            self.send_files_btn.setEnabled(False)
            self.send_folder_btn.setEnabled(False)
            self.send_text_btn.setEnabled(False)
    
    def _activate_sender_tab(self):
        """Activate sender tab if not active"""
        parent_widget = self.parent()
        while parent_widget and not hasattr(parent_widget, 'tabs'):
            parent_widget = parent_widget.parent()
        if parent_widget and hasattr(parent_widget, 'tabs'):
            parent_widget.tabs.setCurrentIndex(0)
    
    def _show_notification(self, message):
        """Show notification that auto-hides after 3 seconds"""
        from PyQt6.QtWidgets import QLabel
        from PyQt6.QtCore import QTimer, Qt
        
        is_dark = self.settings_manager.get("dark_mode", False)
        if is_dark:
            bg = "#238636"
            border = "#2ea043"
        else:
            bg = "#27ae60"
            border = "#2ecc71"
        
        notification = QLabel(message, self)
        notification.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: white;
                padding: 15px 30px;
                border-radius: 8px;
                border: 2px solid {border};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        notification.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notification.setWindowFlags(Qt.WindowType.ToolTip)
        
        # Position at top center of parent window
        parent = self.window()
        x = parent.x() + (parent.width() - 400) // 2
        y = parent.y() + 80
        notification.setGeometry(x, y, 400, 50)
        notification.show()
        
        QTimer.singleShot(3000, notification.deleteLater)
    
    def _toggle_text_input(self):
        """Toggle text input visibility"""
        self.text_card.setVisible(not self.text_card.isVisible())
        if self.text_card.isVisible():
            self.text_input.setFocus()
    
    def _do_send_text(self):
        """Send text as a temp file with special marker"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "تنبيه", "اكتب نصاً أولاً")
            return
        import os, tempfile
        tmp = os.path.join(tempfile.gettempdir(), "__APEX_TEXT__")
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(text)
        self.text_card.setVisible(False)
        self.text_input.clear()
        self._send_files([tmp], is_temp=True)
    
    def cleanup(self):
        """Cleanup on close"""
        if self.sender_worker:
            self.sender_worker.cancel()
        if self.sender_thread and self.sender_thread.is_alive():
            self.sender_thread.join(timeout=1)
        self.is_sending = False  # إعادة تعيين الحماية
