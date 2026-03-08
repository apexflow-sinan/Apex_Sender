"""
Cross-platform service management
"""
import os
import sys
import subprocess
import signal
import time
from pathlib import Path
from ..core.platform_manager import PlatformManager

class CrossPlatformService:
    """Cross-platform service manager"""
    
    SERVICE_NAME = "ApexSenderService"
    SERVICE_DISPLAY_NAME = "Apex Sender Service"
    SERVICE_DESCRIPTION = "خدمة تشغيل Apex Sender في الخلفية"
    
    def __init__(self):
        self.platform = PlatformManager.get_platform()
        self.pid_file = PlatformManager.get_data_dir() / "service.pid"
        
    def is_installed(self):
        """Check if service is installed"""
        if self.platform == "windows":
            try:
                cmd = f'sc query {self.SERVICE_NAME}'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return result.returncode == 0
            except:
                return False
        else:
            # For Linux/macOS, check if systemd service exists or daemon is running
            return self._check_daemon_running()
    
    def install(self):
        """Install service"""
        if self.platform == "windows":
            return self._install_windows_service()
        elif self.platform == "linux":
            return self._install_linux_service()
        elif self.platform == "macos":
            return self._install_macos_service()
        else:
            return False, "منصة غير مدعومة"
    
    def uninstall(self):
        """Uninstall service"""
        if self.platform == "windows":
            return self._uninstall_windows_service()
        elif self.platform == "linux":
            return self._uninstall_linux_service()
        elif self.platform == "macos":
            return self._uninstall_macos_service()
        else:
            return False, "منصة غير مدعومة"
    
    def start(self):
        """Start service"""
        if self.platform == "windows":
            return self._start_windows_service()
        else:
            return self._start_daemon()
    
    def stop(self):
        """Stop service"""
        if self.platform == "windows":
            return self._stop_windows_service()
        else:
            return self._stop_daemon()
    
    def get_status(self):
        """Get service status"""
        if self.platform == "windows":
            return self._get_windows_status()
        else:
            return self._get_daemon_status()
    
    def _install_windows_service(self):
        """Install Windows service"""
        try:
            from .background_service import ApexSenderService
            import win32serviceutil
            
            exe_path = sys.executable if getattr(sys, 'frozen', False) else f'"{sys.executable}" "{Path(__file__).parent / "background_service.py"}"'
            
            if getattr(sys, 'frozen', False):
                cmd = f'"{exe_path}" --install-service-internal'
            else:
                cmd = f'{exe_path} install'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.start()
                return True, "تم تثبيت وتشغيل الخدمة بنجاح"
            else:
                return False, result.stderr or result.stdout
        except Exception as e:
            return False, str(e)
    
    def _install_linux_service(self):
        """Install Linux systemd service"""
        try:
            service_content = f"""[Unit]
Description={self.SERVICE_DESCRIPTION}
After=network.target

[Service]
Type=simple
User=root
ExecStart={sys.executable} {Path(__file__).parent.parent.parent / "main.py"} --service
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
            
            service_file = Path(f"/etc/systemd/system/{self.SERVICE_NAME.lower()}.service")
            
            # Write service file
            with open(service_file, 'w') as f:
                f.write(service_content)
            
            # Reload systemd and enable service
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "enable", f"{self.SERVICE_NAME.lower()}.service"], check=True)
            
            return True, "تم تثبيت الخدمة بنجاح"
        except Exception as e:
            return False, str(e)
    
    def _install_macos_service(self):
        """Install macOS LaunchDaemon"""
        try:
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.apex.sender.service</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{Path(__file__).parent.parent.parent / "main.py"}</string>
        <string>--service</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""
            
            plist_file = Path("/Library/LaunchDaemons/com.apex.sender.service.plist")
            
            # Write plist file
            with open(plist_file, 'w') as f:
                f.write(plist_content)
            
            # Load service
            subprocess.run(["launchctl", "load", str(plist_file)], check=True)
            
            return True, "تم تثبيت الخدمة بنجاح"
        except Exception as e:
            return False, str(e)
    
    def _start_daemon(self):
        """Start daemon process"""
        try:
            if self._check_daemon_running():
                return True, "الخدمة تعمل بالفعل"
            
            # Start daemon process
            cmd = [sys.executable, str(Path(__file__).parent.parent.parent / "main.py"), "--service"]
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Save PID
            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))
            
            return True, "تم بدء الخدمة بنجاح"
        except Exception as e:
            return False, str(e)
    
    def _stop_daemon(self):
        """Stop daemon process"""
        try:
            if not self.pid_file.exists():
                return True, "الخدمة متوقفة بالفعل"
            
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            try:
                os.kill(pid, signal.SIGTERM)
                time.sleep(2)
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            
            self.pid_file.unlink(missing_ok=True)
            return True, "تم إيقاف الخدمة"
        except Exception as e:
            return False, str(e)
    
    def _check_daemon_running(self):
        """Check if daemon is running"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            os.kill(pid, 0)  # Check if process exists
            return True
        except (ProcessLookupError, ValueError, OSError):
            self.pid_file.unlink(missing_ok=True)
            return False
    
    def _get_daemon_status(self):
        """Get daemon status"""
        if self._check_daemon_running():
            return "running"
        else:
            return "stopped"
    
    # Windows service methods (keep existing functionality)
    def _start_windows_service(self):
        try:
            cmd = f'sc start {self.SERVICE_NAME}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "تم بدء الخدمة بنجاح"
            else:
                return False, result.stderr or result.stdout
        except Exception as e:
            return False, str(e)
    
    def _stop_windows_service(self):
        try:
            cmd = f'sc stop {self.SERVICE_NAME}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return True, "تم إيقاف الخدمة"
        except Exception as e:
            return False, str(e)
    
    def _get_windows_status(self):
        try:
            cmd = f'sc query {self.SERVICE_NAME}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout.upper()
                if "RUNNING" in output or ("STATE" in output and "4" in output):
                    return "running"
                elif "STOPPED" in output or ("STATE" in output and "1" in output):
                    return "stopped"
                else:
                    return "unknown"
            else:
                return "not_installed"
        except:
            return "error"
    
    def _uninstall_windows_service(self):
        try:
            self._stop_windows_service()
            
            exe_path = sys.executable if getattr(sys, 'frozen', False) else f'"{sys.executable}" "{Path(__file__).parent / "background_service.py"}"'
            
            if getattr(sys, 'frozen', False):
                cmd = f'"{exe_path}" --uninstall-service-internal'
            else:
                cmd = f'{exe_path} remove'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "تم إلغاء تثبيت الخدمة بنجاح"
            else:
                return False, result.stderr or result.stdout
        except Exception as e:
            return False, str(e)
    
    def _uninstall_linux_service(self):
        try:
            service_file = Path(f"/etc/systemd/system/{self.SERVICE_NAME.lower()}.service")
            
            # Stop and disable service
            subprocess.run(["systemctl", "stop", f"{self.SERVICE_NAME.lower()}.service"], capture_output=True)
            subprocess.run(["systemctl", "disable", f"{self.SERVICE_NAME.lower()}.service"], capture_output=True)
            
            # Remove service file
            if service_file.exists():
                service_file.unlink()
            
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            
            return True, "تم إلغاء تثبيت الخدمة بنجاح"
        except Exception as e:
            return False, str(e)
    
    def _uninstall_macos_service(self):
        try:
            plist_file = Path("/Library/LaunchDaemons/com.apex.sender.service.plist")
            
            # Unload service
            subprocess.run(["launchctl", "unload", str(plist_file)], capture_output=True)
            
            # Remove plist file
            if plist_file.exists():
                plist_file.unlink()
            
            return True, "تم إلغاء تثبيت الخدمة بنجاح"
        except Exception as e:
            return False, str(e)