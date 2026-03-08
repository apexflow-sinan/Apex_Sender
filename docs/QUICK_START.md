# 🚀 Quick Start Guide

## Installation

### Option 1: Run from Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Option 2: Build Executable
```bash
# Build portable version (recommended)
build_portable.bat

# The installer will be in: ApexSender_Installer/
```

## Usage

### Sending Files

1. **Enter Receiver IP**
   - Type IP manually in the boxes
   - Or select from history dropdown

2. **Choose Transfer Type**
   - 📄 **Single File** - Send one file
   - 📋 **Multiple Files** - Send many files at once
   - 📁 **Folder** - Automatically compressed to ZIP

3. **Monitor Progress**
   - Progress bar shows completion
   - Speed indicator shows MB/s
   - Click "إلغاء" to cancel

### Receiving Files

1. **Check Status**
   - Application automatically listens on port 8888
   - Shows "في انتظار اتصال..." when ready

2. **Change Save Location** (Optional)
   - Click "تغيير" to select different folder
   - Default: Documents/ApexSender

3. **Auto-Extract ZIP**
   - Received ZIP files prompt for extraction
   - Or extract automatically if enabled in settings

## Features

### 🎨 Dark Mode
- Toggle in title bar
- Preference saved automatically

### 📱 QR Code
- Click QR icon in title bar
- Share IP easily with mobile devices

### 📊 Transfer Speed
- Real-time speed indicator
- Shows MB/s during transfer

### ⏹️ Cancel Transfer
- Click "إلغاء" button during transfer
- Safely stops ongoing operation

### 📝 IP History
- Last 10 IPs saved automatically
- Select from dropdown for quick access

### 🔊 Sound Notifications
- Success sound on completion
- Error sound on failure
- Can be disabled in settings

## Keyboard Shortcuts

- `Alt+F4` - Close application
- `Ctrl+Tab` - Switch between tabs

## Troubleshooting

### Cannot Connect
- ✅ Both devices on same network
- ✅ Receiver app is running
- ✅ Firewall allows connection
- ✅ Correct IP address entered

### Slow Transfer
- Check network speed
- Close other network applications
- Use wired connection if possible

### Firewall Issues
- Run as administrator
- Allow through Windows Firewall
- Check antivirus settings

## Tips

1. **First Time Setup**
   - Run as administrator for firewall setup
   - Allow through Windows Firewall when prompted

2. **Best Performance**
   - Use wired connection
   - Close unnecessary applications
   - Send multiple small files as ZIP

3. **Security**
   - Only use on trusted networks
   - Verify receiver IP before sending
   - Check received files before opening

## Support

For issues or questions:
- Check README.md for detailed documentation
- Review CHANGELOG.md for recent changes
- Contact development team

## Next Steps

Ready to add enterprise features? See README.md for:
- Adding user authentication
- Creating shared repository
- Implementing chat
- Adding transfer history
