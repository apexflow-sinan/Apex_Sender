import subprocess
import sys
import os
from pathlib import Path

class ServiceInstaller:
    SERVICE_NAME = "ApexSenderService"
    
    @staticmethod
    def _get_executable_path():
        """Get the correct executable path for service installation"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            return sys.executable
        else:
            # Running as script
            return f'"{sys.executable}" "{Path(__file__).parent / "background_service.py"}"'
    
    @staticmethod
    def is_installed():
        try:
            cmd = f'sc query {ServiceInstaller.SERVICE_NAME}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    @staticmethod
    def install():
        try:
            exe_path = ServiceInstaller._get_executable_path()
            if getattr(sys, 'frozen', False):
                cmd = f'"{exe_path}" --install-service-internal'
            else:
                cmd = f'{exe_path} install'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Start the service after installation
                ServiceInstaller.start()
                return True, "تم تثبيت وتشغيل الخدمة بنجاح"
            else:
                return False, result.stderr or result.stdout
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def uninstall():
        try:
            ServiceInstaller.stop()
            
            exe_path = ServiceInstaller._get_executable_path()
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
    
    @staticmethod
    def start():
        try:
            cmd = f'sc start {ServiceInstaller.SERVICE_NAME}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "تم بدء الخدمة بنجاح"
            else:
                return False, result.stderr or result.stdout
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def stop():
        try:
            cmd = f'sc stop {ServiceInstaller.SERVICE_NAME}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return True, "تم إيقاف الخدمة"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_status():
        try:
            cmd = f'sc query {ServiceInstaller.SERVICE_NAME}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout.upper()
                # Check for running state (English and Arabic)
                if "RUNNING" in output or "STATE" in output and "4" in output:
                    return "running"
                # Check for stopped state
                elif "STOPPED" in output or "STATE" in output and "1" in output:
                    return "stopped"
                else:
                    return "unknown"
            else:
                return "not_installed"
        except:
            return "error"
    
    @staticmethod
    def set_auto_start(enable=True):
        try:
            start_type = "auto" if enable else "demand"
            cmd = f'sc config {ServiceInstaller.SERVICE_NAME} start= {start_type}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                msg = "تم تفعيل البدء التلقائي" if enable else "تم تعطيل البدء التلقائي"
                return True, msg
            else:
                return False, result.stderr or result.stdout
        except Exception as e:
            return False, str(e)
