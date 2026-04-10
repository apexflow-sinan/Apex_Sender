"""Menu and dialog stylesheets"""


def get_menu_style(is_dark):
    """Get menu bar stylesheet based on theme"""
    if is_dark:
        return """
            QMenuBar {
                background: #1e1e2e; border: none; font-size: 13px; color: #cdd6f4;
            }
            QMenuBar::item { padding: 8px 15px; border-radius: 5px; background: transparent; }
            QMenuBar::item:selected { background: rgba(102, 126, 234, 0.2); }
            QMenu {
                background: #313244; border: 1px solid #45475a; border-radius: 8px;
                padding: 5px; color: #cdd6f4;
            }
            QMenu::item { padding: 10px 35px 10px 25px; border-radius: 5px; }
            QMenu::item:selected { background: #667eea; color: white; }
            QMenu::separator { height: 1px; background: #45475a; margin: 5px 10px; }
        """
    return """
        QMenuBar { background: transparent; border: none; font-size: 13px; }
        QMenuBar::item { padding: 8px 15px; border-radius: 5px; }
        QMenuBar::item:selected { background: rgba(102, 126, 234, 0.1); }
        QMenu {
            background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 5px;
        }
        QMenu::item { padding: 10px 35px 10px 25px; border-radius: 5px; }
        QMenu::item:selected { background: #667eea; color: white; }
        QMenu::separator { height: 1px; background: #e0e0e0; margin: 5px 10px; }
    """


def get_setup_dialog_style(is_dark):
    """Get setup dialog stylesheet based on theme"""
    if is_dark:
        return """
            QDialog { background: #1e1e2e; color: #cdd6f4; }
            QLabel { color: #cdd6f4; }
            QLabel#headerLabel { color: #667eea; }
            QGroupBox {
                font-weight: bold; font-size: 13px; border: 2px solid #45475a;
                border-radius: 8px; margin-top: 10px; padding-top: 10px; color: #cdd6f4;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
            QCheckBox { color: #cdd6f4; spacing: 8px; }
            QCheckBox::indicator {
                width: 18px; height: 18px; border-radius: 4px;
                border: 2px solid #45475a; background: #313244;
            }
            QCheckBox::indicator:checked { background: #667eea; border-color: #667eea; }
            QPushButton#actionButton {
                background: #313244; color: #cdd6f4; border: 1px solid #45475a;
                padding: 8px 15px; border-radius: 5px; font-size: 12px;
            }
            QPushButton#actionButton:hover { background: #45475a; border-color: #667eea; }
            QPushButton#saveButton {
                background: #667eea; color: white; border: none;
                padding: 10px 25px; border-radius: 5px; font-weight: bold; font-size: 13px;
            }
            QPushButton#saveButton:hover { background: #5568d3; }
            QPushButton#applyButton {
                background: #27ae60; color: white; border: none;
                padding: 10px 25px; border-radius: 5px; font-weight: bold; font-size: 13px;
            }
            QPushButton#applyButton:hover { background: #229954; }
            QPushButton#cancelButton {
                background: #45475a; color: #cdd6f4; border: none;
                padding: 10px 25px; border-radius: 5px; font-weight: bold; font-size: 13px;
            }
            QPushButton#cancelButton:hover { background: #585b70; }
        """
    return """
        QDialog { background: white; color: #2c3e50; }
        QLabel#headerLabel { color: #667eea; }
        QGroupBox {
            font-weight: bold; font-size: 13px; border: 2px solid #e0e0e0;
            border-radius: 8px; margin-top: 10px; padding-top: 10px; color: #2c3e50;
        }
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        QCheckBox { color: #2c3e50; spacing: 8px; }
        QCheckBox::indicator {
            width: 18px; height: 18px; border-radius: 4px;
            border: 2px solid #bdc3c7; background: white;
        }
        QCheckBox::indicator:checked { background: #667eea; border-color: #667eea; }
        QPushButton#actionButton {
            background: #f8f9fa; color: #2c3e50; border: 1px solid #dee2e6;
            padding: 8px 15px; border-radius: 5px; font-size: 12px;
        }
        QPushButton#actionButton:hover { background: #e9ecef; border-color: #667eea; }
        QPushButton#saveButton {
            background: #667eea; color: white; border: none;
            padding: 10px 25px; border-radius: 5px; font-weight: bold; font-size: 13px;
        }
        QPushButton#saveButton:hover { background: #5568d3; }
        QPushButton#applyButton {
            background: #27ae60; color: white; border: none;
            padding: 10px 25px; border-radius: 5px; font-weight: bold; font-size: 13px;
        }
        QPushButton#applyButton:hover { background: #229954; }
        QPushButton#cancelButton {
            background: #95a5a6; color: white; border: none;
            padding: 10px 25px; border-radius: 5px; font-weight: bold; font-size: 13px;
        }
        QPushButton#cancelButton:hover { background: #7f8c8d; }
    """
