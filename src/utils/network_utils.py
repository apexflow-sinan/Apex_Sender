"""Network utility functions"""
import socket

def get_local_ip():
    """Get local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def get_all_ips():
    """Get all network interfaces with their IPs (name, ip)"""
    results = []
    try:
        import psutil
        for name, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith('127.') and not addr.address.startswith('169.254.'):
                    results.append((name, addr.address))
    except Exception:
        results.append(("Default", get_local_ip()))
    return results if results else [("Default", get_local_ip())]

def check_connection(host, port, timeout=3):
    """Check if connection to host:port is possible"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False
