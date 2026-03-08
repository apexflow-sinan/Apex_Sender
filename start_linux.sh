#!/bin/bash
# Simple launcher for Apex Sender on Linux

# Suppress Qt warnings
export QT_LOGGING_RULES="qt.qpa.xcb.warning=false"
export QT_QPA_PLATFORM_PLUGIN_PATH=""

# Run the application
python3 main.py "$@" 2>/dev/null