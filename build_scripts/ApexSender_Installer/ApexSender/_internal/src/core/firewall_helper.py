import subprocess
import sys
import os
from .platform_manager import PlatformManager

try:
    import ctypes
except ImportError:
    ctypes = None

class FirewallHelper:
    APP_NAME = "Apex Sender"
    
    @staticmethod
    def is_admin():
        platform = PlatformManager.get_platform()
        
        if platform == "windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() if ctypes else False
            except:
                return False
        elif platform in ["linux", "macos"]:
            try:
                return os.geteuid() == 0
            except AttributeError:
                # os.geteuid() not available on this platform
                return False
        return False
    
    @staticmethod
    def run_as_admin():
        if FirewallHelper.is_admin():
            return False
            
        platform = PlatformManager.get_platform()
        
        if platform == "windows" and ctypes:
            try:
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                return True
            except:
                return False
        elif platform in ["linux", "macos"]:
            print("يرجى تشغيل البرنامج باستخدام sudo للحصول على صلاحيات المسؤول")
            print("Please run with sudo for administrator privileges")
            return False
        return False
    
    @staticmethod
    def check_firewall_rule(port):
        platform = PlatformManager.get_platform()
        
        try:
            if platform == "windows":
                cmd = f'netsh advfirewall firewall show rule name="{FirewallHelper.APP_NAME} Port {port}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return result.returncode == 0
            elif platform == "linux":
                try:
                    # Check ufw status
                    result = subprocess.run(["ufw", "status"], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0 and str(port) in result.stdout:
                        return True
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
                try:
                    # Check iptables
                    result = subprocess.run(["iptables", "-L", "-n"], capture_output=True, text=True, timeout=5)
                    return str(port) in result.stdout
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
                return False
            elif platform == "macos":
                # macOS doesn't require firewall rules for most apps
                return True
        except:
            pass
        return False
    
    @staticmethod
    def add_firewall_rule(port, protocol="TCP"):
        platform = PlatformManager.get_platform()
        
        if platform == "windows":
            if not FirewallHelper.is_admin():
                return False, "يجب تشغيل البرنامج كمسؤول"
            
            try:
                rule_name = f"{FirewallHelper.APP_NAME} Port {port}"
                cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol={protocol} localport={port}'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    return True, f"تم إضافة قاعدة جدار الحماية للمنفذ {port}"
                else:
                    return False, result.stderr
            except Exception as e:
                return False, str(e)
                
        elif platform == "linux":
            if not FirewallHelper.is_admin():
                return False, "يجب تشغيل البرنامج بصلاحيات المسؤول (sudo)"
            
            try:
                # Try ufw first
                result = subprocess.run(["ufw", "allow", str(port)], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return True, f"تم إضافة قاعدة جدار الحماية للمنفذ {port}"
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            
            try:
                # Fallback to iptables
                cmd = f"iptables -A INPUT -p {protocol.lower()} --dport {port} -j ACCEPT"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return True, f"تم إضافة قاعدة جدار الحماية للمنفذ {port}"
                else:
                    return False, result.stderr
            except Exception as e:
                return False, str(e)
                
        elif platform == "macos":
            # macOS typically doesn't need firewall rules for local apps
            return True, f"لا حاجة لإعداد جدار الحماية على macOS للمنفذ {port}"
            
        return False, "منصة غير مدعومة"
    
    @staticmethod
    def remove_firewall_rule(port):
        platform = PlatformManager.get_platform()
        
        if platform == "windows":
            if not FirewallHelper.is_admin():
                return False, "يجب تشغيل البرنامج كمسؤول"
            
            try:
                rule_name = f"{FirewallHelper.APP_NAME} Port {port}"
                cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    return True, f"تم حذف قاعدة جدار الحماية للمنفذ {port}"
                else:
                    return False, result.stderr
            except Exception as e:
                return False, str(e)
                
        elif platform == "linux":
            if not FirewallHelper.is_admin():
                return False, "يجب تشغيل البرنامج بصلاحيات المسؤول (sudo)"
            
            try:
                # Try ufw first
                result = subprocess.run(["ufw", "delete", "allow", str(port)], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return True, f"تم حذف قاعدة جدار الحماية للمنفذ {port}"
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            
            try:
                # Fallback to iptables
                cmd = f"iptables -D INPUT -p tcp --dport {port} -j ACCEPT"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return True, f"تم حذف قاعدة جدار الحماية للمنفذ {port}"
                else:
                    return False, result.stderr
            except Exception as e:
                return False, str(e)
                
        elif platform == "macos":
            return True, f"لا حاجة لحذف قواعد جدار الحماية على macOS للمنفذ {port}"
            
        return False, "منصة غير مدعومة"
    
    @staticmethod
    def check_all_ports(ports):
        results = {}
        for port in ports:
            results[port] = FirewallHelper.check_firewall_rule(port)
        return results
    
    @staticmethod
    def add_all_rules(ports):
        platform = PlatformManager.get_platform()
        
        if platform in ["windows", "linux"] and not FirewallHelper.is_admin():
            admin_msg = "يجب تشغيل البرنامج كمسؤول" if platform == "windows" else "يجب تشغيل البرنامج بصلاحيات المسؤول (sudo)"
            return False, admin_msg
        
        results = []
        for port in ports:
            success, msg = FirewallHelper.add_firewall_rule(port)
            results.append((port, success, msg))
        
        all_success = all(r[1] for r in results)
        return all_success, results
