#!/bin/bash
# Video Upscaler Pro - Installation Script for Linux/macOS
# This script sets up the Python virtual environment and installs dependencies

set -e  # Exit on error

echo "========================================"
echo "Video Upscaler Pro - Installation"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Please install Python 3.10 or higher"
    echo ""
    echo "On Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "On macOS: brew install python@3.10"
    exit 1
fi

echo "[1/5] Checking Python version..."
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Python version: $PYTHON_VERSION"

# Check if version is 3.10+
MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
    echo -e "${RED}ERROR: Python 3.10 or higher is required${NC}"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo -e "${GREEN}✓ Python version OK${NC}"

echo ""
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Removing old one...${NC}"
    rm -rf venv
fi

python3 -m venv venv

if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
    echo "Try installing python3-venv: sudo apt install python3-venv"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment created${NC}"

echo ""
echo "[3/5] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[4/5] Upgrading pip..."
pip install --upgrade pip

echo ""
echo "[5/5] Installing dependencies..."
echo "This may take several minutes..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}ERROR: Failed to install dependencies${NC}"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================"
echo "Installation completed successfully!"
echo "========================================${NC}"
echo ""
echo "To start the application, run:"
echo "  ./start.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
