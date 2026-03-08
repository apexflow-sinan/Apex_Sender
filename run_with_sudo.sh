#!/bin/bash
# Apex Sender - Run with sudo helper

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "🔒 يتطلب صلاحيات المسؤول..."
    echo "🔒 Root privileges required..."
    
    # Try to re-run with sudo
    if command -v sudo &> /dev/null; then
        echo "🚀 إعادة التشغيل بصلاحيات sudo..."
        sudo -E python3 main.py "$@"
    elif command -v pkexec &> /dev/null; then
        echo "🚀 إعادة التشغيل بصلاحيات pkexec..."
        pkexec python3 main.py "$@"
    else
        echo "❌ لم يتم العثور على sudo أو pkexec"
        echo "❌ sudo or pkexec not found"
        exit 1
    fi
else
    # Already running as root
    python3 main.py "$@"
fi
