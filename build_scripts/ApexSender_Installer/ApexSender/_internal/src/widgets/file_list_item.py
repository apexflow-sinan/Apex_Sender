"""Received files list widget"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QApplication
)
from PyQt6.QtCore import Qt, QTimer
import qtawesome as qta


class ReceivedFileItem(QFrame):
    """Single received file/text item widget"""

    def __init__(self, file_info, on_delete, parent=None):
        super().__init__(parent)
        self.setObjectName("fileItem")
        self.file_info = file_info
        layout = QVBoxLayout(self)
        layout.setSpacing(5)

        if file_info.get("type") == "text":
            self._build_text_item(layout, file_info, on_delete)
        else:
            self._build_file_item(layout, file_info, on_delete)

    def _build_text_item(self, layout, info, on_delete):
        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("💬"))
        name_row.addWidget(QLabel("رسالة نصية"), 1)
        layout.addLayout(name_row)

        text_label = QLabel(info.get("text", ""))
        text_label.setWordWrap(True)
        text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text_label.setStyleSheet(
            "padding: 8px; background: rgba(99,102,241,0.08); border-radius: 6px; font-size: 13px;"
        )
        layout.addWidget(text_label)

        bottom = QHBoxLayout()
        time_label = QLabel(info.get("_time_str", ""))
        time_label.setStyleSheet("color: #888; font-size: 11px;")
        bottom.addWidget(time_label)
        bottom.addStretch()

        copy_btn = QPushButton(qta.icon('fa5s.copy'), " نسخ")
        copy_btn.setMaximumWidth(80)
        copy_btn.clicked.connect(lambda: self._copy_with_feedback(copy_btn, info.get("text", "")))
        bottom.addWidget(copy_btn)

        del_btn = QPushButton(qta.icon('fa5s.trash', color='#e74c3c'), "")
        del_btn.setMaximumWidth(40)
        del_btn.setToolTip("حذف")
        del_btn.clicked.connect(lambda: on_delete(info, self))
        bottom.addWidget(del_btn)
        layout.addLayout(bottom)

    def _copy_with_feedback(self, btn, text):
        QApplication.clipboard().setText(text)
        original_icon = btn.icon()
        original_text = btn.text()
        btn.setIcon(qta.icon('fa5s.check', color='#2ecc71'))
        btn.setText(" تم النسخ")
        btn.setStyleSheet("color: #2ecc71; font-weight: bold;")
        QTimer.singleShot(1500, lambda: (
            btn.setIcon(original_icon),
            btn.setText(original_text),
            btn.setStyleSheet("")
        ))

    def _build_file_item(self, layout, info, on_delete):
        from src.utils.system_utils import open_file_or_folder

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel(_file_icon(info["filename"])))
        name_label = QLabel(info["filename"])
        name_label.setWordWrap(True)
        name_row.addWidget(name_label, 1)
        layout.addLayout(name_row)

        time_label = QLabel(info.get("_time_str", ""))
        time_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(time_label)

        btn_row = QHBoxLayout()
        open_file_btn = QPushButton("فتح الملف")
        open_file_btn.setMaximumWidth(120)
        open_file_btn.clicked.connect(lambda: open_file_or_folder(info["filepath"]))
        btn_row.addWidget(open_file_btn)

        open_folder_btn = QPushButton("فتح المجلد")
        open_folder_btn.setMaximumWidth(120)
        open_folder_btn.clicked.connect(lambda: open_file_or_folder(os.path.dirname(info["filepath"])))
        btn_row.addWidget(open_folder_btn)

        del_btn = QPushButton(qta.icon('fa5s.trash', color='#e74c3c'), "")
        del_btn.setMaximumWidth(40)
        del_btn.setToolTip("حذف الملف")
        del_btn.clicked.connect(lambda: on_delete(info, self))
        btn_row.addWidget(del_btn)
        layout.addLayout(btn_row)


def _file_icon(filename):
    ext = os.path.splitext(filename)[1].lower()
    icons = {
        '.pdf': '📄', '.doc': '📄', '.docx': '📄', '.txt': '📄',
        '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
        '.zip': '📦', '.rar': '📦', '.7z': '📦',
        '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬',
        '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵',
    }
    return icons.get(ext, '📁')
