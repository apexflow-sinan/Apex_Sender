"""Platform-specific messages"""
from src.core.platform_manager import PlatformManager

class PlatformMessages:
    """Provides platform-specific user messages"""
    
    @staticmethod
    def get_admin_required_short():
        """Get short admin required message"""
        platform = PlatformManager.get_platform()
        
        if platform == "windows":
            return "يجب تشغيل البرنامج كمسؤول (Administrator)"
        else:
            return "يجب تشغيل البرنامج بصلاحيات الجذر (Root/sudo)"
    
    @staticmethod
    def get_admin_required_detailed():
        """Get detailed admin required message"""
        platform = PlatformManager.get_platform()
        
        if platform == "windows":
            return "يجب تشغيل البرنامج كمسؤول (Administrator)\n\nانقر بزر الماوس الأيمن على البرنامج واختر 'Run as Administrator'"
        elif platform == "linux":
            return "يجب تشغيل البرنامج بصلاحيات الجذر (Root)\n\nاستخدم الأمر:\nsudo python main.py"
        else:  # macOS
            return "يجب تشغيل البرنامج بصلاحيات المسؤول\n\nاستخدم الأمر:\nsudo python main.py"
    
    @staticmethod
    def get_service_name():
        """Get platform-specific service name"""
        platform = PlatformManager.get_platform()
        
        if platform == "windows":
            return "Windows Service"
        elif platform == "linux":
            return "Systemd Service"
        else:  # macOS
            return "Launch Daemon"
    
    @staticmethod
    def get_firewall_name():
        """Get platform-specific firewall name"""
        platform = PlatformManager.get_platform()
        
        if platform == "windows":
            return "Windows Firewall"
        elif platform == "linux":
            return "Firewall (ufw/iptables)"
        else:  # macOS
            return "macOS Firewall"
