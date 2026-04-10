# Apex Sender - Fast File Transfer Application

## 📁 Project Structure

```
Apex Sender/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── PNG.png                 # Project icon preview
│
├── src/                    # Source code
│   ├── config/             # Configuration
│   │   ├── settings.py     # App settings & constants
│   │   └── styles.py       # UI stylesheets (Light/Dark)
│   │
│   ├── core/               # Core functionality
│   │   ├── settings_manager.py   # Settings persistence
│   │   ├── config_manager.py     # Config management
│   │   ├── status_manager.py     # App status tracking
│   │   ├── firewall_helper.py    # Firewall configuration
│   │   ├── platform_manager.py   # Cross-platform support
│   │   └── server_manager.py     # Server management
│   │
│   ├── network/            # Network operations
│   │   ├── signals.py      # Qt signals (file_received, text_received)
│   │   ├── sender.py       # File/text sender thread
│   │   └── receiver.py     # File/text receiver thread
│   │
│   ├── service/            # Background service
│   │   ├── cross_platform_service.py
│   │   ├── background_service.py
│   │   └── service_installer.py
│   │
│   ├── ui/                 # User interface
│   │   ├── main_window.py      # Main window
│   │   ├── sender_tab.py       # Send files & text
│   │   ├── receiver_tab.py     # Receive files & text
│   │   ├── web_tab.py          # Web server control
│   │   ├── games_tab.py        # Games server control
│   │   ├── qr_dialog.py        # QR code dialog
│   │   ├── setup_dialog.py     # Advanced settings
│   │   ├── about_dialog.py     # About dialog
│   │   └── help_dialog.py      # Help dialog
│   │
│   ├── utils/              # Utilities
│   │   ├── network_utils.py     # Network helpers
│   │   ├── file_utils.py        # File operations
│   │   ├── file_dialog_utils.py # File dialog helpers
│   │   ├── qr_utils.py          # QR code generation
│   │   ├── sound_utils.py       # Sound notifications
│   │   ├── system_utils.py      # System operations
│   │   ├── server_diagnostics.py # Port diagnostics
│   │   └── platform_messages.py  # Platform messages
│   │
│   ├── widgets/            # Reusable widgets
│   │   └── loading_indicator.py
│   │
│   └── version.py          # Version info
│
├── web/                    # Web interface
│   ├── server.py           # Flask web server + API
│   └── templates/          # HTML templates
│       └── index_bottom_nav.html  # Responsive web UI
│
├── assets/                 # Application assets
│   ├── icons/              # App icons (PNG, ICO)
│   └── sounds/             # Sound files
│
├── config/                 # Default configuration
│   └── default_settings.json
│
├── scripts/                # Utility scripts
│   ├── start.bat           # Windows start
│   ├── start_linux.sh      # Linux start
│   ├── run.sh / run_with_sudo.sh
│   ├── allow_firewall.bat  # Firewall setup
│   ├── install_service.bat / uninstall_service.bat
│   ├── check_dependencies.py
│   └── download_sounds.py
│
├── build_scripts/          # Build & deployment
│   ├── build.bat           # Build single exe
│   ├── build_portable.bat  # Build portable
│   ├── build_fast.bat      # Fast build
│   ├── install_template.bat
│   └── clean.bat
│
├── docs/                   # Documentation
│   ├── QUICK_START.md
│   ├── TROUBLESHOOTING.md
│   └── SEND_PROTECTION.md
│
└── ApexGames/              # Integrated games server
```

## ✨ Features

- ✅ Fast file transfer over local network
- ✅ Send/receive text messages (chat-like)
- ✅ Send single, multiple files, or folders
- ✅ Auto-compress folders to ZIP
- ✅ Transfer speed indicator (MB/s)
- ✅ Web interface (responsive: desktop sidebar + mobile bottom nav)
- ✅ QR Code for easy IP sharing
- ✅ Dark/Light mode with persistent settings
- ✅ Window size/position persistence
- ✅ Sound notifications
- ✅ Automatic firewall configuration
- ✅ Background service support (Windows/Linux/macOS)
- ✅ Integrated games server

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## 📦 Dependencies

- PyQt6 — GUI framework
- qtawesome — Icon library
- qrcode + Pillow — QR code generation
- Flask — Web server
- requests — HTTP client
- psutil — System utilities
- pywin32 — Windows service (Windows only)
