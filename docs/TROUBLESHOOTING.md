# Troubleshooting Guide

## Application Won't Start

### Step 1: Check Dependencies
```bash
python check_dependencies.py
```

If any packages are missing, install them:
```bash
pip install -r requirements.txt
```

### Step 2: Run in Debug Mode
```bash
debug_start.bat
```

This will show any error messages.

### Step 3: Check Python Version
```bash
python --version
```

Required: Python 3.8 or higher

### Step 4: Test Simple Window
```bash
python -c "from PyQt6.QtWidgets import QApplication, QLabel; import sys; app = QApplication(sys.argv); w = QLabel('Test'); w.show(); sys.exit(app.exec())"
```

If this doesn't work, PyQt6 installation is broken.

## Common Issues

### Issue: "No module named 'PyQt6'"
**Solution:**
```bash
pip install PyQt6
```

### Issue: "No module named 'src'"
**Solution:** Make sure you're running from the project root directory:
```bash
cd "d:\Apex sender"
python main.py
```

### Issue: Application starts but window doesn't appear
**Solution:** Check if another instance is running:
- Close all Python processes
- Try again

### Issue: "Port 8888 already in use"
**Solution:** 
- Close other instances of the app
- Or change DEFAULT_PORT in `src/config/settings.py`

### Issue: Firewall blocks connection
**Solution:**
- Run as administrator
- Allow through Windows Firewall when prompted

## Debug Commands

### Check if port is in use:
```bash
netstat -ano | findstr :8888
```

### Kill process using port:
```bash
taskkill /PID <process_id> /F
```

### Reinstall all dependencies:
```bash
pip uninstall -y PyQt6 qtawesome qrcode Pillow
pip install -r requirements.txt
```

## Still Not Working?

1. Delete `settings.json` and try again
2. Run `debug_start.bat` and share the error message
3. Check if antivirus is blocking Python
4. Try running as administrator

## Contact

If none of these solutions work, provide:
- Output of `python check_dependencies.py`
- Output of `debug_start.bat`
- Python version
- Windows version
