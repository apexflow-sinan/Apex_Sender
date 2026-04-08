import threading
import logging
from typing import Optional, Tuple
from .config_manager import ConfigManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerManager:
    def __init__(self):
        self.config = ConfigManager()
        self.web_server_thread: Optional[threading.Thread] = None
        self.network_server_thread: Optional[threading.Thread] = None
        self.running = False
    
    def start_web_server(self, port: int = None):
        if port is None:
            port = self.config.get('web_port', 8080)
        
        try:
            import sys
            import os
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            
            from web.server import start_server
            self.web_server_thread = threading.Thread(
                target=start_server,
                args=(port,),
                daemon=True
            )
            self.web_server_thread.start()
            logger.info(f"Web server started on port {port}")
            return True, f"Web server started on port {port}"
        except Exception as e:
            logger.error(f"Failed to start web server: {e}")
            return False, str(e)
    
    def start_network_server(self, port: int = None, save_dir: str = None):
        if port is None:
            port = self.config.get('network_port', 9999)
        
        try:
            from src.network.receiver import FileReceiver
            receiver = FileReceiver(port=port, save_directory=save_dir)
            
            self.network_server_thread = threading.Thread(
                target=receiver.start,
                daemon=True
            )
            self.network_server_thread.start()
            logger.info(f"Network server started on port {port}")
            return True, f"Network server started on port {port}"
        except Exception as e:
            logger.error(f"Failed to start network server: {e}")
            return False, str(e)
    
    def start_all(self, web_port: int = None, network_port: int = None, save_dir: str = None):
        results = []
        
        web_success, web_msg = self.start_web_server(web_port)
        results.append(('web', web_success, web_msg))
        
        net_success, net_msg = self.start_network_server(network_port, save_dir)
        results.append(('network', net_success, net_msg))
        
        self.running = web_success and net_success
        return self.running, results
    
    def stop_all(self):
        self.running = False
        logger.info("Servers stopped")
        return True, "Servers stopped"
    
    def get_status(self):
        return {
            'running': self.running,
            'web_server': self.web_server_thread is not None and self.web_server_thread.is_alive(),
            'network_server': self.network_server_thread is not None and self.network_server_thread.is_alive(),
            'web_port': self.config.get('web_port', 8080),
            'network_port': self.config.get('network_port', 9999)
        }
