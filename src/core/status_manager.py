"""Status manager for application state"""
from enum import Enum
from PyQt6.QtCore import QObject, pyqtSignal

class AppStatus(Enum):
    """Application status states"""
    IDLE = "idle"
    READY_TO_SEND = "ready_to_send"
    READY_TO_RECEIVE = "ready_to_receive"
    CHECKING_CONNECTION = "checking_connection"
    COMPRESSING = "compressing"
    SENDING = "sending"
    RECEIVING = "receiving"
    CANCELLING = "cancelling"
    SUCCESS = "success"
    ERROR = "error"

class StatusManager(QObject):
    """Manage application status and emit changes"""
    status_changed = pyqtSignal(str, str, str)  # status_text, icon, color
    
    def __init__(self):
        super().__init__()
        self._current_status = AppStatus.IDLE
        self._status_messages = {
            AppStatus.IDLE: ("جاهز", "fa5s.circle", "#95a5a6"),
            AppStatus.READY_TO_SEND: ("جاهز للإرسال", "fa5s.paper-plane", "#3498db"),
            AppStatus.READY_TO_RECEIVE: ("جاهز للاستقبال", "fa5s.download", "#2ecc71"),
            AppStatus.CHECKING_CONNECTION: ("فحص الاتصال...", "fa5s.sync", "#f39c12"),
            AppStatus.COMPRESSING: ("جاري الضغط...", "fa5s.file-archive", "#9b59b6"),
            AppStatus.SENDING: ("جاري الإرسال...", "fa5s.upload", "#3498db"),
            AppStatus.RECEIVING: ("جاري الاستقبال...", "fa5s.download", "#2ecc71"),
            AppStatus.CANCELLING: ("جاري الإلغاء...", "fa5s.times-circle", "#e67e22"),
            AppStatus.SUCCESS: ("تم بنجاح", "fa5s.check-circle", "#27ae60"),
            AppStatus.ERROR: ("خطأ", "fa5s.exclamation-circle", "#e74c3c"),
        }
    
    def set_status(self, status: AppStatus, custom_message: str = None):
        """Set current status and emit signal"""
        self._current_status = status
        message, icon, color = self._status_messages[status]
        
        if custom_message:
            message = custom_message
        
        self.status_changed.emit(message, icon, color)
    
    def set_custom_status(self, message: str, icon: str = "fa5s.info-circle", color: str = "#3498db"):
        """Set custom status"""
        self.status_changed.emit(message, icon, color)
    
    def get_current_status(self) -> AppStatus:
        """Get current status"""
        return self._current_status
    
    def is_busy(self) -> bool:
        """Check if application is busy"""
        return self._current_status in [
            AppStatus.CHECKING_CONNECTION,
            AppStatus.COMPRESSING,
            AppStatus.SENDING,
            AppStatus.RECEIVING,
            AppStatus.CANCELLING
        ]
