"""UI Stylesheets"""

LIGHT_STYLESHEET = """
QWidget {
    font-family: Segoe UI;
    font-size: 11pt;
    color: #2c3e50;
    background-color: #f0f2f5;
}
QMainWindow {
    background-color: #f0f2f5;
}
QLabel {
    background-color: transparent;
}
#TitleBar {
    background-color: #2c3e50;
}
#TitleBar QLabel {
    color: white;
}
#TitleLabel {
    font-size: 18pt;
    font-weight: bold;
    padding: 10px;
}
#IPLabel {
    font-size: 10pt;
    color: #1abc9c;
    padding-bottom: 10px;
}
QTabWidget {
    background-color: #f0f2f5;
}
QTabWidget::pane {
    border: none;
    background-color: #f0f2f5;
}
QTabBar {
    background-color: #f0f2f5;
}
QTabBar::tab {
    background: #e1e4e8;
    color: #586069;
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
    border-bottom: 3px solid transparent;
}
QTabBar::tab:selected {
    background: #ffffff;
    color: #2c3e50;
    border-bottom: 3px solid #27ae60;
}
#TabContent {
    background-color: #ffffff;
    border-radius: 8px;
    border-top-left-radius: 0px;
    padding: 15px;
}
QFrame[objectName="card"] {
    background-color: #f6f8fa;
    border: 1px solid #d1d5da;
    border-radius: 6px;
    padding: 10px;
}
QFrame[objectName="card"] QLabel {
    color: #2c3e50;
}
QPushButton {
    background-color: #27ae60;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 6px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2ecc71;
}
QPushButton:disabled {
    background-color: #95a5a6;
}
QPushButton#DangerButton {
    background-color: #e74c3c;
}
QPushButton#DangerButton:hover {
    background-color: #c0392b;
}
QPushButton#CancelButton {
    background-color: #e67e22;
}
QPushButton#CancelButton:hover {
    background-color: #d35400;
}
QLineEdit {
    border: 1px solid #d1d5da;
    border-radius: 6px;
    padding: 8px;
    background-color: #fff;
    color: #2c3e50;
}
QComboBox {
    border: 1px solid #d1d5da;
    border-radius: 6px;
    padding: 8px;
    background-color: #fff;
    color: #2c3e50;
}
QComboBox::drop-down {
    border: none;
}
QComboBox QAbstractItemView {
    background-color: #fff;
    color: #2c3e50;
    selection-background-color: #27ae60;
}
QProgressBar {
    border: 1px solid #d1d5da;
    border-radius: 6px;
    text-align: center;
    background-color: #e1e4e8;
    color: #2c3e50;
}
QProgressBar::chunk {
    background-color: #27ae60;
    border-radius: 6px;
}
QTextEdit {
    background-color: #24292e;
    color: #f6f8fa;
    border-radius: 6px;
    font-family: Consolas, Courier New, monospace;
    max-height: 150px;
}
QCheckBox {
    color: #2c3e50;
}
QPushButton[flat="true"] {
    background-color: transparent;
    border: none;
    text-align: left;
    padding: 0;
}
QPushButton[flat="true"]:hover {
    background-color: #e8eaed;
}
QStatusBar {
    background-color: #f6f8fa;
    border-top: 1px solid #d1d5da;
    color: #586069;
}
QStatusBar QLabel {
    padding: 2px 5px;
}
QMessageBox {
    background-color: #ffffff;
}
QMessageBox QLabel {
    color: #2c3e50;
}
QTextEdit#logEdit {
    border: 1px solid #d1d5da;
    border-radius: 6px;
    margin: 5px;
}
QFrame[objectName="fileItem"] {
    background-color: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    padding: 10px;
    margin: 3px;
}
QFrame[objectName="fileItem"] QPushButton {
    padding: 6px 12px;
    font-size: 10pt;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
"""

DARK_STYLESHEET = """
QWidget {
    font-family: Segoe UI;
    font-size: 11pt;
    color: #ecf0f1;
    background-color: #1e1e1e;
}
QMainWindow {
    background-color: #1e1e1e;
}
QLabel {
    background-color: transparent;
    color: #ecf0f1;
}
#TitleBar {
    background-color: #0d1117;
}
#TitleBar QLabel {
    color: white;
}
#TitleLabel {
    font-size: 18pt;
    font-weight: bold;
    padding: 10px;
}
#IPLabel {
    font-size: 10pt;
    color: #1abc9c;
    padding-bottom: 10px;
}
QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    background: #2d2d2d;
    color: #a0a0a0;
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
    border-bottom: 3px solid transparent;
}
QTabBar::tab:selected {
    background: #161b22;
    color: #ecf0f1;
    border-bottom: 3px solid #238636;
}
#TabContent {
    background-color: #161b22;
    border-radius: 8px;
    border-top-left-radius: 0px;
    padding: 15px;
}
QFrame[objectName="card"] {
    background-color: #21262d;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 10px;
}
QFrame[objectName="card"] QLabel {
    color: #ecf0f1;
}
QPushButton {
    background-color: #238636;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 6px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2ea043;
}
QPushButton:disabled {
    background-color: #484f58;
}
QPushButton#DangerButton {
    background-color: #da3633;
}
QPushButton#DangerButton:hover {
    background-color: #b62324;
}
QPushButton#CancelButton {
    background-color: #e67e22;
}
QPushButton#CancelButton:hover {
    background-color: #d35400;
}
QLineEdit {
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px;
    background-color: #0d1117;
    color: #ecf0f1;
}
QComboBox {
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px;
    background-color: #0d1117;
    color: #ecf0f1;
}
QComboBox::drop-down {
    border: none;
}
QComboBox QAbstractItemView {
    background-color: #161b22;
    color: #ecf0f1;
    selection-background-color: #238636;
}
QProgressBar {
    border: 1px solid #30363d;
    border-radius: 6px;
    text-align: center;
    background-color: #21262d;
    color: #ecf0f1;
}
QProgressBar::chunk {
    background-color: #238636;
    border-radius: 6px;
}
QTextEdit {
    background-color: #0d1117;
    color: #c9d1d9;
    border-radius: 6px;
    font-family: Consolas, Courier New, monospace;
    max-height: 150px;
    border: 1px solid #30363d;
}
QCheckBox {
    color: #ecf0f1;
}
QPushButton[flat="true"] {
    background-color: transparent;
    border: none;
    text-align: left;
    padding: 0;
}
QPushButton[flat="true"]:hover {
    background-color: #2d2d2d;
}
QStatusBar {
    background-color: #21262d;
    border-top: 1px solid #30363d;
    color: #8b949e;
}
QStatusBar QLabel {
    padding: 2px 5px;
    color: #8b949e;
}
QMessageBox {
    background-color: #161b22;
}
QMessageBox QLabel {
    color: #ecf0f1;
}
QTextEdit#logEdit {
    border: 1px solid #30363d;
    border-radius: 6px;
    margin: 5px;
}
QFrame[objectName="fileItem"] {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 10px;
    margin: 3px;
}
QFrame[objectName="fileItem"] QPushButton {
    padding: 6px 12px;
    font-size: 10pt;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
"""
