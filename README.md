# Apex Sender - Fast File Transfer Application with Integrated Games Server

## 📁 Project Structure

```
Apex sender/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── app_icon.ico           # Application icon
│
├── src/                   # Source code
│   ├── config/           # Configuration files
│   │   ├── settings.py   # App settings & constants
│   │   └── styles.py     # UI stylesheets (Light/Dark)
│   │
│   ├── core/             # Core functionality
│   │   └── settings_manager.py  # Settings persistence
│   │
│   ├── network/          # Network operations
│   │   ├── signals.py    # Qt signals
│   │   ├── sender.py     # File sender thread
│   │   └── receiver.py   # File receiver thread
│   │
│   ├── ui/               # User interface
│   │   ├── main_window.py    # Main window
│   │   ├── sender_tab.py     # Sender tab
│   │   ├── receiver_tab.py   # Receiver tab
│   │   └── qr_dialog.py      # QR code dialog
│   │
│   └── utils/            # Utility functions
│       ├── network_utils.py  # Network helpers
│       ├── file_utils.py     # File operations
│       ├── qr_utils.py       # QR code generation
│       └── sound_utils.py    # Sound notifications
│
├── assets/               # Application assets
│   └── sounds/          # Sound files
│
└── build scripts/        # Build & deployment
    ├── build.bat        # Build single exe
    └── build_portable.bat  # Build portable version
```

## ✨ Features

### Current Features
- ✅ Fast file transfer over local network
- ✅ Send single or multiple files
- ✅ Send folders (auto-compressed to ZIP)
- ✅ Auto-extract received ZIP files
- ✅ Transfer speed indicator (MB/s)
- ✅ Cancel transfer option
- ✅ IP history (last 10 IPs)
- ✅ QR Code for easy IP sharing
- ✅ Dark Mode support
- ✅ Sound notifications
- ✅ Persistent settings
- ✅ Automatic firewall configuration
- ✅ Modern & responsive UI

### Planned Features (Enterprise)
- 📋 Shared file repository
- 👥 User management
- 🔐 Authentication & encryption
- 📊 Transfer history & analytics
- 💬 Chat functionality
- 🔔 Desktop notifications
- 🌐 Multi-language support

## 🚀 Quick Start

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Build
```bash
# Build portable version (recommended)
build_portable.bat

# Build single executable
build.bat
```

## 📝 Adding New Features

### 1. Add Network Feature
- Create new file in `src/network/`
- Use `WorkerSignals` for thread communication
- Follow existing sender/receiver pattern

### 2. Add UI Component
- Create new file in `src/ui/`
- Inherit from appropriate Qt widget
- Use settings_manager for persistence

### 3. Add Utility Function
- Add to appropriate file in `src/utils/`
- Keep functions pure and reusable
- Add docstrings

### 4. Modify Settings
- Update `src/config/settings.py` for constants
- Update `src/core/settings_manager.py` for persistent settings

## 🎨 Customization

### Change Theme Colors
Edit `src/config/styles.py`:
- `LIGHT_STYLESHEET` for light mode
- `DARK_STYLESHEET` for dark mode

### Change Network Settings
Edit `src/config/settings.py`:
- `DEFAULT_PORT` - Change default port
- `BUFFER_SIZE` - Adjust transfer buffer
- `CONNECTION_TIMEOUT` - Connection timeout

## 📦 Dependencies

- PyQt6 - GUI framework
- qtawesome - Icon library
- qrcode - QR code generation
- Pillow - Image processing

## 🔧 Configuration Files

- `settings.json` - User preferences (auto-created)
- `history.json` - IP history (deprecated, moved to settings)

## 📄 License

Proprietary - For internal company use only

## 👨‍💻 Development

### Code Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings to all functions
- Keep functions small and focused

### Testing
```bash
# Run application in development mode
python main.py

# Test specific module
python -m src.utils.file_utils
```

## 🐛 Troubleshooting

### Import Errors
Make sure all `__init__.py` files exist in src folders

### Firewall Issues
Run application as administrator for automatic firewall setup

### Build Issues
Clean build artifacts: `clean.bat`

## 📞 Support

For issues or feature requests, contact the development team.
