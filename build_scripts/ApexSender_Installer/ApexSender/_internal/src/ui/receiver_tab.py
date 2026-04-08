"""Receiver tab widget"""
import os
import json
from datetime import datetime
import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QProgressBar, QFrame, QMessageBox, QFileDialog, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from src.core.status_manager import AppStatus
from src.utils.file_utils import extract_zip
from src.utils.sound_utils import play_success_sound, play_notification_sound
from src.utils.file_dialog_utils import get_existing_directory

class ReceiverTab(QWidget):
    """Receiver tab widget"""
    
    def __init__(self, settings_manager, status_manager, log_callback):
        super().__init__()
        self.settings_manager = settings_manager
        self.status_manager = status_manager
        self.log_callback = log_callback
        self.received_files = []
        self.setObjectName("TabContent")
        self.load_received_files()
        self.setup_ui()
        
        # Timer for auto-reset
        self.reset_timer = QTimer()
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.reset_ui)
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        
        # Status card
        card = QFrame(objectName="card")
        card_layout = QVBoxLayout(card)
        
        # Status icon and text
        status_layout = QHBoxLayout()
        self.status_icon = QLabel()
        self.status_icon.setPixmap(qta.icon('fa5s.download', color='#2ecc71').pixmap(32, 32))
        status_layout.addWidget(self.status_icon)
        
        status_text_layout = QVBoxLayout()
        status_text_layout.addWidget(QLabel("حالة الاستقبال:", objectName="CardTitle"))
        self.status_label = QLabel("جاهز لاستقبال الملفات")
        status_text_layout.addWidget(self.status_label)
        status_layout.addLayout(status_text_layout)
        status_layout.addStretch()
        
        card_layout.addLayout(status_layout)
        layout.addWidget(card)
        
        # Save directory
        dir_card = QFrame(objectName="card")
        dir_layout = QVBoxLayout(dir_card)
        dir_layout.addWidget(QLabel("مجلد الحفظ:", objectName="CardTitle"))
        
        dir_path_layout = QHBoxLayout()
        self.dir_label = QLabel(self.settings_manager.get("save_directory"))
        self.dir_label.setWordWrap(True)
        dir_path_layout.addWidget(self.dir_label)
        
        change_dir_btn = QPushButton(qta.icon('fa5s.folder-open'), "")
        change_dir_btn.setMaximumWidth(40)
        change_dir_btn.setToolTip("تغيير مجلد الحفظ")
        change_dir_btn.clicked.connect(self.change_save_directory)
        dir_path_layout.addWidget(change_dir_btn)
        
        dir_layout.addLayout(dir_path_layout)
        layout.addWidget(dir_card)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("في انتظار الملفات...", alignment=Qt.AlignmentFlag.AlignCenter)
        self.speed_label = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.speed_label)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.open_folder_btn = QPushButton(qta.icon('fa5s.folder-open'), " فتح مجلد الحفظ")
        self.open_folder_btn.clicked.connect(self.open_save_folder)
        action_layout.addWidget(self.open_folder_btn)
        
        self.delete_files_btn = QPushButton(qta.icon('fa5s.trash', color='white'), " حذف الملفات")
        self.delete_files_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        self.delete_files_btn.clicked.connect(self.delete_files)
        self.delete_files_btn.setEnabled(len(self.received_files) > 0)
        action_layout.addWidget(self.delete_files_btn)
        
        layout.addLayout(action_layout)
        
        # Received files list
        files_card = QFrame(objectName="card")
        files_layout = QVBoxLayout(files_card)
        files_layout.addWidget(QLabel("📥 الملفات المستلمة", objectName="CardTitle"))
        
        # Scroll area for files
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(300)
        
        self.files_container = QWidget()
        self.files_list_layout = QVBoxLayout(self.files_container)
        self.files_list_layout.setSpacing(5)
        self.files_list_layout.addStretch()
        
        scroll.setWidget(self.files_container)
        files_layout.addWidget(scroll)
        
        layout.addWidget(files_card)
        self.refresh_files_list()
    
    def change_save_directory(self):
        """Change save directory"""
        current_dir = self.settings_manager.get("save_directory")
        new_dir = get_existing_directory(self, "اختر مجلد الحفظ", current_dir)
        
        if new_dir:
            self.settings_manager.set("save_directory", new_dir)
            self.dir_label.setText(new_dir)
            self.log_callback(f"تم تغيير مجلد الحفظ إلى: {new_dir}")
    
    def open_save_folder(self):
        """Open save folder in file explorer"""
        from src.utils.system_utils import open_file_or_folder
        
        save_dir = self.settings_manager.get("save_directory")
        success, error = open_file_or_folder(save_dir)
        
        if not success:
            QMessageBox.warning(self, "خطأ", f"فشل فتح المجلد: {error}")
    
    def delete_single_file(self, file_info, item_frame):
        """Delete a single file"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("حذف الملف")
        msg.setText(f"هل تريد حذف {file_info['filename']}؟")
        
        from_app_btn = msg.addButton("حذف من التطبيق فقط", QMessageBox.ButtonRole.YesRole)
        from_folder_btn = msg.addButton("حذف من المجلد أيضاً", QMessageBox.ButtonRole.DestructiveRole)
        cancel_btn = msg.addButton("إلغاء", QMessageBox.ButtonRole.RejectRole)
        
        msg.exec()
        clicked = msg.clickedButton()
        
        if clicked == cancel_btn:
            return
        
        delete_from_disk = (clicked == from_folder_btn)
        
        # Second confirmation if deleting from disk
        if delete_from_disk:
            reply = QMessageBox.warning(
                self, "تأكيد الحذف",
                f"هل أنت متأكد من حذف الملف من المجلد؟\n{file_info['filename']}\n\nلا يمكن التراجع عن هذا الإجراء!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
            
            # Delete from disk
            try:
                if os.path.exists(file_info["filepath"]):
                    os.remove(file_info["filepath"])
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل حذف الملف:\n{str(e)}")
                return
        
        # Remove from list
        self.received_files.remove(file_info)
        self.save_received_files()
        
        # Remove UI element
        item_frame.deleteLater()
        
        msg_text = "تم حذف الملف من المجلد" if delete_from_disk else "تم حذف الملف من التطبيق"
        QMessageBox.information(self, "تم الحذف", msg_text)
    
    def delete_files(self):
        """Delete received files"""
        if not self.received_files:
            QMessageBox.information(self, "لا توجد ملفات", "لا توجد ملفات مستلمة للحذف")
            return
        
        # First confirmation
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("حذف الملفات")
        msg.setText("هل ترغب في حذف الملفات؟")
        
        from_app_btn = msg.addButton("حذف من التطبيق فقط", QMessageBox.ButtonRole.YesRole)
        from_folder_btn = msg.addButton("حذف من المجلد أيضاً", QMessageBox.ButtonRole.DestructiveRole)
        cancel_btn = msg.addButton("إلغاء", QMessageBox.ButtonRole.RejectRole)
        
        msg.exec()
        clicked = msg.clickedButton()
        
        if clicked == cancel_btn:
            return
        
        delete_from_disk = (clicked == from_folder_btn)
        
        # Second confirmation if deleting from disk
        if delete_from_disk:
            reply = QMessageBox.warning(
                self, "تأكيد الحذف",
                f"هل أنت متأكد من حذف {len(self.received_files)} ملف من المجلد؟\nلا يمكن التراجع عن هذا الإجراء!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Perform deletion
        deleted_count = 0
        failed_files = []
        
        if delete_from_disk:
            for file_info in self.received_files:
                try:
                    if os.path.exists(file_info["filepath"]):
                        os.remove(file_info["filepath"])
                        deleted_count += 1
                except Exception as e:
                    failed_files.append(file_info["filename"])
        
        # Clear from app
        self.received_files.clear()
        self.save_received_files()
        self.refresh_files_list()
        
        # Show result
        if delete_from_disk:
            if failed_files:
                QMessageBox.warning(
                    self, "حذف جزئي",
                    f"تم حذف {deleted_count} ملف\nفشل حذف {len(failed_files)} ملف"
                )
            else:
                QMessageBox.information(self, "تم الحذف", f"تم حذف {deleted_count} ملف من المجلد")
        else:
            QMessageBox.information(self, "تم الحذف", "تم حذف السجل من التطبيق")
    
    def update_progress(self, value, text, speed):
        """Update progress"""
        self._activate_receiver_tab()
        self.progress_bar.setValue(value)
        self.progress_label.setText(text)
        self.speed_label.setText(f"السرعة: {speed:.2f} MB/s")
        self.status_manager.set_status(AppStatus.RECEIVING)
    
    @pyqtSlot(str)
    def on_finished(self, message: str):
        """Handle transfer finished"""
        self.progress_label.setText(message)
        self.speed_label.setText("")
        
        if "بنجاح" in message:
            self.status_manager.set_status(AppStatus.SUCCESS)
            play_success_sound()
            self.refresh_files_list()
            # Auto-reset after 3 seconds
            self.reset_timer.start(3000)
        else:
            self.status_manager.set_status(AppStatus.ERROR)
            # Auto-reset after 5 seconds
            self.reset_timer.start(5000)
    
    @pyqtSlot(str)
    def ask_extract(self, zip_path: str):
        """Ask user if they want to extract ZIP file"""
        if not self.settings_manager.get("auto_extract_zip", True):
            return
        
        reply = QMessageBox.question(
            self, "استخراج الملف المضغوط",
            f"هل تريد استخراج الملف المضغوط؟\\n{os.path.basename(zip_path)}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                extract_dir = extract_zip(zip_path)
                self.log_callback(f"تم استخراج الملف إلى: {extract_dir}")
                QMessageBox.information(self, "تم الاستخراج", f"تم استخراج الملف بنجاح إلى:\\n{extract_dir}")
            except Exception as e:
                self.log_callback(f"فشل استخراج الملف: {e}")
                QMessageBox.critical(self, "خطأ", f"فشل استخراج الملف:\\n{e}")
    
    def reset_ui(self):
        """Reset UI to ready state"""
        self.progress_bar.setValue(0)
        self.progress_label.setText("في انتظار الملفات...")
        self.speed_label.setText("")
        self.status_manager.set_status(AppStatus.READY_TO_RECEIVE)
    
    def load_received_files(self):
        """Load received files history"""
        history_file = os.path.join(self.settings_manager.get("save_directory"), ".apex_history.json")
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.received_files = json.load(f)
            except:
                self.received_files = []
    
    def save_received_files(self):
        """Save received files history"""
        history_file = os.path.join(self.settings_manager.get("save_directory"), ".apex_history.json")
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.received_files[-20:], f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def add_received_file(self, filename, filepath):
        """Add file to received list"""
        file_info = {
            "filename": filename,
            "filepath": filepath,
            "timestamp": datetime.now().isoformat(),
            "size": os.path.getsize(filepath) if os.path.exists(filepath) else 0
        }
        self.received_files.insert(0, file_info)
        self.save_received_files()
        self.delete_files_btn.setEnabled(True)
    
    def refresh_files_list(self):
        """Refresh the files list display"""
        # Clear existing items
        while self.files_list_layout.count() > 1:
            item = self.files_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add files
        for file_info in self.received_files[:20]:
            self.add_file_item(file_info)
        
        # Update delete button state
        self.delete_files_btn.setEnabled(len(self.received_files) > 0)
    
    def add_file_item(self, file_info):
        """Add a file item to the list"""
        from src.utils.system_utils import open_file_or_folder
        
        item_frame = QFrame()
        item_frame.setObjectName("fileItem")
        item_layout = QVBoxLayout(item_frame)
        item_layout.setSpacing(5)
        
        # File name with icon
        name_layout = QHBoxLayout()
        icon = self.get_file_icon(file_info["filename"])
        name_layout.addWidget(QLabel(icon))
        name_label = QLabel(file_info["filename"])
        name_label.setWordWrap(True)
        name_layout.addWidget(name_label, 1)
        item_layout.addLayout(name_layout)
        
        # Time
        time_str = self.format_time(file_info["timestamp"])
        time_label = QLabel(time_str)
        time_label.setStyleSheet("color: #888; font-size: 11px;")
        item_layout.addWidget(time_label)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        open_file_btn = QPushButton("فتح الملف")
        open_file_btn.clicked.connect(lambda: open_file_or_folder(file_info["filepath"]))
        btn_layout.addWidget(open_file_btn)
        
        open_folder_btn = QPushButton("فتح المجلد")
        open_folder_btn.clicked.connect(lambda: open_file_or_folder(os.path.dirname(file_info["filepath"])))
        btn_layout.addWidget(open_folder_btn)
        
        delete_btn = QPushButton(qta.icon('fa5s.trash', color='#e74c3c'), "")
        delete_btn.setMaximumWidth(40)
        delete_btn.setToolTip("حذف الملف")
        delete_btn.clicked.connect(lambda: self.delete_single_file(file_info, item_frame))
        btn_layout.addWidget(delete_btn)
        
        item_layout.addLayout(btn_layout)
        
        self.files_list_layout.insertWidget(0, item_frame)
    
    def get_file_icon(self, filename):
        """Get icon based on file extension"""
        ext = os.path.splitext(filename)[1].lower()
        icons = {
            '.pdf': '📄', '.doc': '📄', '.docx': '📄', '.txt': '📄',
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
            '.zip': '📦', '.rar': '📦', '.7z': '📦',
            '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬',
            '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵',
        }
        return icons.get(ext, '📁')
    
    def format_time(self, timestamp):
        """Format timestamp to readable string"""
        try:
            dt = datetime.fromisoformat(timestamp)
            now = datetime.now()
            diff = now - dt
            
            if diff.days == 0:
                if diff.seconds < 60:
                    return "الآن"
                elif diff.seconds < 3600:
                    return f"منذ {diff.seconds // 60} دقيقة"
                else:
                    return f"منذ {diff.seconds // 3600} ساعة"
            elif diff.days == 1:
                return "أمس"
            else:
                return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return "---"
    
    def _activate_receiver_tab(self):
        """Activate receiver tab if not active"""
        parent_widget = self.parent()
        while parent_widget and not hasattr(parent_widget, 'tabs'):
            parent_widget = parent_widget.parent()
        if parent_widget and hasattr(parent_widget, 'tabs'):
            parent_widget.tabs.setCurrentIndex(1)
    
    def cleanup(self):
        """Cleanup on close"""
        if self.reset_timer.isActive():
            self.reset_timer.stop()