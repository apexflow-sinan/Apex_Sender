"""Worker thread for service/firewall operations"""
from PyQt6.QtCore import QThread, pyqtSignal
from src.core.firewall_helper import FirewallHelper


class ServiceWorker(QThread):
    """Worker thread for service operations"""
    finished = pyqtSignal(bool, str)

    def __init__(self, action, config=None):
        super().__init__()
        self.action = action
        self.config = config

    def run(self):
        try:
            if self.action == "install":
                from src.service.cross_platform_service import CrossPlatformService
                success, msg = CrossPlatformService().install()
                self.finished.emit(success, msg)
            elif self.action == "uninstall":
                from src.service.cross_platform_service import CrossPlatformService
                success, msg = CrossPlatformService().uninstall()
                self.finished.emit(success, msg)
            elif self.action == "add_firewall":
                ports = [self.config.get('web_port', 8080), self.config.get('network_port', 9999)]
                success, _ = FirewallHelper.add_all_rules(ports)
                self.finished.emit(success, "تم إضافة قواعد جدار الحماية بنجاح" if success else "فشل في إضافة بعض القواعد")
            elif self.action == "check_firewall":
                ports = [self.config.get('web_port', 8080), self.config.get('network_port', 9999)]
                results = FirewallHelper.check_all_ports(ports)
                if all(results.values()):
                    self.finished.emit(True, "✅ جدار الحماية مُعد بشكل صحيح")
                else:
                    missing = [str(p) for p, ok in results.items() if not ok]
                    self.finished.emit(False, f"⚠️ المنافذ التالية تحتاج إعداد: {', '.join(missing)}")
        except ImportError:
            self.finished.emit(False, "خدمة الخلفية غير متوفرة في هذا الإصدار")
        except Exception as e:
            self.finished.emit(False, str(e))
