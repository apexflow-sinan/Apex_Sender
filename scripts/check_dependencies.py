"""Check if all dependencies are installed"""
import sys

print("Checking dependencies...\n")

required = {
    'PyQt6': 'PyQt6',
    'qtawesome': 'qtawesome',
    'qrcode': 'qrcode',
    'PIL': 'Pillow'
}

missing = []
for module, package in required.items():
    try:
        __import__(module)
        print(f"✓ {package} - OK")
    except ImportError:
        print(f"✗ {package} - MISSING")
        missing.append(package)

print("\n" + "="*50)

if missing:
    print(f"\nMissing packages: {', '.join(missing)}")
    print("\nInstall with:")
    print(f"pip install {' '.join(missing)}")
    sys.exit(1)
else:
    print("\n✓ All dependencies installed!")
    print("\nTrying to import application modules...")
    
    try:
        from src.config import settings
        print("✓ src.config.settings")
        
        from src.core.settings_manager import SettingsManager
        print("✓ src.core.settings_manager")
        
        from src.utils.network_utils import get_local_ip
        print("✓ src.utils.network_utils")
        ip = get_local_ip()
        print(f"  Local IP: {ip}")
        
        from src.ui.main_window import MainWindow
        print("✓ src.ui.main_window")
        
        print("\n✓ All modules loaded successfully!")
        print("\nApplication should work. Try running:")
        print("  python main.py")
        
    except Exception as e:
        print(f"\n✗ Error loading modules: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
