#!/usr/bin/env python3
"""Server Diagnostics - تشخيص مشاكل السيرفر"""
import socket
import subprocess
import sys

def check_port_available(port):
    """فحص إذا كان المنفذ متاح"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
            return True, f"المنفذ {port} متاح"
    except OSError:
        return False, f"المنفذ {port} مستخدم من برنامج آخر"

def check_flask_installed():
    """فحص تثبيت Flask"""
    try:
        import flask
        return True, f"Flask مثبت (الإصدار {flask.__version__})"
    except ImportError:
        return False, "Flask غير مثبت - قم بتثبيته: pip install flask"

def get_process_using_port(port):
    """معرفة البرنامج المستخدم للمنفذ"""
    try:
        if sys.platform == 'win32':
            result = subprocess.run(
                ['netstat', '-ano'], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    # Get process name
                    proc = subprocess.run(
                        ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV', '/NH'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if proc.stdout:
                        name = proc.stdout.split(',')[0].strip('"')
                        return f"البرنامج: {name} (PID: {pid})"
        else:
            result = subprocess.run(
                ['lsof', '-i', f':{port}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout:
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    return lines[1].split()[0]
    except:
        pass
    return "غير معروف"

def diagnose_server_issue(port, server_name="السيرفر"):
    """تشخيص شامل لمشاكل السيرفر"""
    issues = []
    
    # 1. فحص المنفذ
    port_ok, port_msg = check_port_available(port)
    if not port_ok:
        process = get_process_using_port(port)
        issues.append(f"❌ {port_msg}\n   {process}")
    
    # 2. فحص Flask
    flask_ok, flask_msg = check_flask_installed()
    if not flask_ok:
        issues.append(f"❌ {flask_msg}")
    
    # 3. فحص الاتصال بالشبكة
    try:
        socket.gethostbyname(socket.gethostname())
    except:
        issues.append("❌ مشكلة في الاتصال بالشبكة")
    
    return issues

def get_alternative_port(start_port, max_attempts=10):
    """البحث عن منفذ بديل متاح"""
    for port in range(start_port, start_port + max_attempts):
        if check_port_available(port)[0]:
            return port
    return None
