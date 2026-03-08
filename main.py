#!/usr/bin/env python3
"""
Apex Sender - Fast File Transfer Application with Integrated Games Server
Main entry point
"""
import sys
import os
import traceback

# Fix paths for PyInstaller
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    if hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
    else:
        os.chdir(os.path.dirname(sys.executable))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QLockFile, QDir

# Suppress Qt warnings
os.environ['QT_LOGGING_RULES'] = 'qt.qpa.xcb.warning=false;qt.qpa.xcb=false;*.warning=false'

# Global lock file
lock_file = None

def check_single_instance():
    """Check if another instance is already running"""
    global lock_file
    
    # Create lock file in temp directory
    lock_path = os.path.join(QDir.tempPath(), 'ApexSender.lock')
    lock_file = QLockFile(lock_path)
    
    # Try to lock
    if not lock_file.tryLock(100):
        return False
    
    return True

def run_service_mode():
    """Run in service mode (servers only, no GUI)"""
    from src.core.server_manager import ServerManager
    import time
    
    print("Starting Apex Sender in service mode...")
    manager = ServerManager()
    success, results = manager.start_all()
    
    if success:
        print("Servers started successfully")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping servers...")
            manager.stop_all()
    else:
        print(f"Failed to start servers: {results}")
        sys.exit(1)

def show_setup_dialog():
    """Show setup dialog only"""
    from src.ui.setup_dialog import SetupDialog
    from PyQt6.QtWidgets import QApplication as QApp
    
    app = QApp(sys.argv)
    app.setApplicationName("Apex Sender Setup")
    
    dialog = SetupDialog()
    dialog.exec()
    sys.exit(0)

def install_service():
    """Install service (cross-platform)"""
    from src.service.cross_platform_service import CrossPlatformService
    from src.core.firewall_helper import FirewallHelper
    from src.core.platform_manager import PlatformManager
    from src.config.settings import DEFAULT_PORT
    
    platform = PlatformManager.get_platform()
    
    # Check admin privileges
    if platform in ["windows", "linux", "macos"] and not FirewallHelper.is_admin():
        if platform == "windows":
            print("خطأ: يجب تشغيل البرنامج كمسؤول (Administrator)")
            print("Error: Administrator privileges required")
        else:
            print("خطأ: يجب تشغيل البرنامج بصلاحيات الجذر (Root)")
            print("Error: Root privileges required. Please run with sudo")
        sys.exit(1)
    
    # Check and add firewall rule
    if not FirewallHelper.check_firewall_rule(DEFAULT_PORT):
        print(f"إضافة قاعدة جدار الحماية للمنفذ {DEFAULT_PORT}...")
        fw_success, fw_msg = FirewallHelper.add_firewall_rule(DEFAULT_PORT)
        print(fw_msg)
    
    service = CrossPlatformService()
    success, msg = service.install()
    print(msg)
    sys.exit(0 if success else 1)

def uninstall_service():
    """Uninstall service (cross-platform)"""
    from src.service.cross_platform_service import CrossPlatformService
    from src.core.firewall_helper import FirewallHelper
    from src.core.platform_manager import PlatformManager
    
    platform = PlatformManager.get_platform()
    
    # Check admin privileges
    if platform in ["windows", "linux", "macos"] and not FirewallHelper.is_admin():
        if platform == "windows":
            print("خطأ: يجب تشغيل البرنامج كمسؤول (Administrator)")
            print("Error: Administrator privileges required")
        else:
            print("خطأ: يجب تشغيل البرنامج بصلاحيات الجذر (Root)")
            print("Error: Root privileges required. Please run with sudo")
        sys.exit(1)
    
    service = CrossPlatformService()
    success, msg = service.uninstall()
    print(msg)
    sys.exit(0 if success else 1)

def main():
    """Main application entry point"""
    # Check command line arguments
    if "--service" in sys.argv:
        run_service_mode()
        return
    
    if "--setup" in sys.argv:
        show_setup_dialog()
        return
    
    if "--install-service" in sys.argv:
        from src.core.firewall_helper import FirewallHelper
        from src.core.platform_manager import PlatformManager
        
        platform = PlatformManager.get_platform()
        
        if platform == "windows" and not FirewallHelper.is_admin():
            try:
                import ctypes
                # Windows-specific elevation
                windll = getattr(ctypes, 'windll', None)
                if windll:
                    windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)  # type: ignore
                    sys.exit(0)
            except (ImportError, AttributeError, OSError):
                print("خطأ: يجب تشغيل البرنامج كمسؤول (Administrator)")
                sys.exit(1)
        elif platform in ["linux", "macos"] and not FirewallHelper.is_admin():
            print("خطأ: يجب تشغيل البرنامج بصلاحيات الجذر (Root)")
            print("Error: Root privileges required. Please run with sudo")
            sys.exit(1)
        
        install_service()
        return
    
    if "--uninstall-service" in sys.argv:
        uninstall_service()
        return
    
    # Internal service commands (used by service installer - Windows only)
    if "--install-service-internal" in sys.argv:
        from src.core.platform_manager import PlatformManager
        if PlatformManager.is_windows():
            try:
                from src.service.background_service import ApexSenderService
                import win32serviceutil  # type: ignore
                sys.argv = [sys.argv[0], 'install']
                win32serviceutil.HandleCommandLine(ApexSenderService)
            except ImportError:
                print("خطأ: مكتبات Windows غير متوفرة")
                sys.exit(1)
        return
    
    if "--uninstall-service-internal" in sys.argv:
        from src.core.platform_manager import PlatformManager
        if PlatformManager.is_windows():
            try:
                from src.service.background_service import ApexSenderService
                import win32serviceutil  # type: ignore
                sys.argv = [sys.argv[0], 'remove']
                win32serviceutil.HandleCommandLine(ApexSenderService)
            except ImportError:
                print("خطأ: مكتبات Windows غير متوفرة")
                sys.exit(1)
        return
    
    # Normal GUI mode
    try:
        from src.ui.main_window import MainWindow
        from PyQt6.QtWidgets import QApplication as QApp
        
        # Suppress Qt platform warnings
        os.environ.setdefault('QT_QPA_PLATFORM_PLUGIN_PATH', '')
        
        app = QApp(sys.argv)
        app.setApplicationName("Apex Sender")
        app.setOrganizationName("Apex")
        
        # Check for single instance
        if not check_single_instance():
            QMessageBox.warning(
                None,
                "Apex Sender",
                "التطبيق يعمل بالفعل!\n\nApex Sender is already running!"
            )
            sys.exit(0)
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
    
    except Exception as e:
        # Show error dialog
        existing_app = QApplication.instance()
        app = existing_app if existing_app else QApplication(sys.argv)
        error_msg = f"Error starting application:\n\n{str(e)}\n\nSee console for details."
        QMessageBox.critical(None, "Apex Sender - Error", error_msg)
        
        # Print full traceback
        print("="*50)
        print("ERROR STARTING APPLICATION")
        print("="*50)
        traceback.print_exc()
        print("="*50)
        
        sys.exit(1)

if __name__ == "__main__":
    main()
