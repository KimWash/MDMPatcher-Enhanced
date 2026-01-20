#!/bin/bash
# MDMPatcher Enhanced - Windows Edition Launcher (for Git Bash / WSL)

echo "========================================"
echo "MDMPatcher Enhanced - Windows Edition"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.8 or higher from python.org"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Python: OK"
echo ""

# Check if dependencies are installed
if ! python -c "import PyQt6" &> /dev/null; then
    echo "Installing dependencies..."
    python -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to install dependencies"
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo ""
fi

echo "Dependencies: OK"
echo ""

# Launch the application
echo "Launching MDMPatcher Enhanced..."
echo ""
python main.py

# If application exits with error, pause
if [ $? -ne 0 ]; then
    echo ""
    echo "Application exited with error"
    read -p "Press Enter to exit..."
fi
