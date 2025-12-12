#!/bin/bash
# Video Upscaler Pro - Start Script for Linux/macOS

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo "Video Upscaler Pro"
echo "========================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}ERROR: Virtual environment not found${NC}"
    echo "Please run ./install.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo -e "${RED}ERROR: app.py not found${NC}"
    echo "The application may not be properly installed"
    exit 1
fi

# Start the application
echo -e "${GREEN}Starting Video Upscaler Pro...${NC}"
echo ""
echo "The application will open in your browser automatically."
echo "To stop the application, press Ctrl+C in this terminal."
echo ""

python app.py

# Check exit code
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}ERROR: Application exited with an error${NC}"
    exit 1
fi
