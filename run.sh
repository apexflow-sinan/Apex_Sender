#!/bin/bash
# Apex Sender - Cross-Platform File Transfer
# Linux/macOS launcher script

echo "🚀 Apex Sender - Cross-Platform File Transfer"
echo "=================================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "Please install python3-venv: sudo apt install python3-venv"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Check if dependencies are installed
DEPS_INSTALLED="venv/.deps_installed"
if [ ! -f "$DEPS_INSTALLED" ]; then
    echo "📥 Installing dependencies (first time only)..."
    
    # Determine which requirements file to use
    if [ -f "requirements.txt" ]; then
        REQ_FILE="requirements.txt"
    elif [ -f "requirements-base.txt" ]; then
        REQ_FILE="requirements-base.txt"
    else
        echo "❌ No requirements file found"
        exit 1
    fi
    
    echo "Using $REQ_FILE..."
    pip install -r "$REQ_FILE"
    
    if [ $? -eq 0 ]; then
        touch "$DEPS_INSTALLED"
        echo "✅ Dependencies installed successfully"
    else
        echo "❌ Failed to install dependencies"
        echo "Try running: pip install -r $REQ_FILE"
        exit 1
    fi
else
    echo "✅ Dependencies already installed"
fi

# Set Qt environment variables to suppress warnings
export QT_LOGGING_RULES="qt.qpa.xcb.warning=false;qt.qpa.xcb=false;*.warning=false"
export QT_QPA_PLATFORM_PLUGIN_PATH=""

# Run the application
echo "✨ Starting Apex Sender..."
echo ""
python3 main.py "$@"

EXIT_CODE=$?

# Deactivate virtual environment
deactivate

exit $EXIT_CODE