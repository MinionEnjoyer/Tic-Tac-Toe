#!/bin/bash
# Installation script for Tic-Tac-Toe Raspberry Pi Zero 2 W
# Run with: sudo bash install.sh

echo "=========================================="
echo "Tic-Tac-Toe Game - Installation Script"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "ERROR: Please run as root (use sudo)"
    exit 1
fi

echo "Step 1: Updating system packages..."
apt update && apt upgrade -y

echo ""
echo "Step 2: Installing system dependencies..."
apt install -y python3-pip python3-dev python3-setuptools scons swig

echo ""
echo "Step 3: Installing Python packages..."
pip3 install -r requirements.txt

echo ""
echo "Step 4: Making main.py executable..."
chmod +x main.py

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "IMPORTANT: You still need to:"
echo "1. Enable SPI interface:"
echo "   sudo raspi-config"
echo "   → Interface Options → SPI → Enable"
echo ""
echo "2. Disable audio to free PWM pins:"
echo "   sudo nano /boot/config.txt"
echo "   Comment out: #dtparam=audio=on"
echo "   Add these lines:"
echo "   dtoverlay=pwm,pin=12,func=4"
echo "   dtoverlay=pwm-2chan,pin=18,func=2,pin2=19,func2=2"
echo ""
echo "3. Reboot your Raspberry Pi:"
echo "   sudo reboot"
echo ""
echo "After reboot, run the game with:"
echo "   sudo python3 main.py"
echo ""
echo "See README.md for complete documentation."
echo "=========================================="
