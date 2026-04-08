import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.apex_sender'
        self.config_file = self.config_dir / 'server_config.json'
        self.default_config = {
            'web_port': 8080,
            'network_port': 9999,
            'auto_start': False,
            'run_as_service': False,
            'firewall_configured': False
        }
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**self.default_config, **json.load(f)}
            except:
                return self.default_config.copy()
        return self.default_config.copy()
    
    def save_config(self, config):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    
    def get(self, key, default=None):
        config = self.load_config()
        return config.get(key, default)
    
    def set(self, key, value):
        config = self.load_config()
        config[key] = value
        self.save_config(config)
