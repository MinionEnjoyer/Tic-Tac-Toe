# Quick Start Guide - Tic-Tac-Toe Raspberry Pi Zero 2 W

## Fast Setup (5 minutes)

### 1. Transfer Files to Raspberry Pi
```bash
# From your computer, copy the project folder to your Pi
scp -r tictactoe-raspi pi@raspberrypi.local:~/
```

### 2. Connect to Your Raspberry Pi
```bash
ssh pi@raspberrypi.local
cd ~/tictactoe-raspi
```

### 3. Run Installation Script
```bash
sudo bash install.sh
```

### 4. Configure System Settings

#### Enable SPI
```bash
sudo raspi-config
```
- Navigate to: **Interface Options** → **SPI** → **Enable**
- Select **Finish** but DON'T reboot yet

#### Disable Audio (Free PWM Pins)
```bash
sudo nano /boot/config.txt
```

Find and comment out:
```
#dtparam=audio=on
```

Add at the end:
```
# Disable audio to free PWM pins for NeoPixels
dtoverlay=pwm,pin=12,func=4
dtoverlay=pwm-2chan,pin=18,func=2,pin2=19,func2=2
```

Save: `Ctrl+X`, then `Y`, then `Enter`

### 5. Reboot
```bash
sudo reboot
```

### 6. Run the Game!
After reboot, SSH back in and run:
```bash
cd ~/tictactoe-raspi
sudo python3 main.py
```

## Hardware Checklist

Before powering on, verify:

- [ ] All 9 LED matrices connected to power (5V + GND)
- [ ] 1000µF capacitor installed on each matrix power line
- [ ] Three data lines from Raspberry Pi GPIO through SN74AHCT125N buffer
- [ ] 330Ω resistors on each data line (before buffer input)
- [ ] All 9 buttons wired to their respective GPIO pins and GND
- [ ] Two turn indicator LEDs with 330Ω resistors connected to GPIO 16 and 20
- [ ] 5V 10A power supply connected
- [ ] Fuse installed in line with power

## GPIO Quick Reference

### Buttons (Connect to GND when pressed)
```
0: GPIO17  1: GPIO27  2: GPIO22
3: GPIO23  4: GPIO24  5: GPIO25
6: GPIO5   7: GPIO6   8: GPIO13
```

### LED Data (Through Buffer)
```
Row 0 (Panels 0,1,2): GPIO12
Row 1 (Panels 3,4,5): GPIO18
Row 2 (Panels 6,7,8): GPIO19
```

### Turn Indicators
```
Red LED (X):  GPIO16
Blue LED (O): GPIO20
```

## Troubleshooting Quick Fixes

### LEDs Don't Work
```bash
# Check SPI is enabled
ls /dev/spidev*

# Should show: /dev/spidev0.0  /dev/spidev0.1

# If not, enable SPI and reboot
sudo raspi-config  # Interface Options → SPI → Enable
sudo reboot
```

### Permission Errors
```bash
# Always use sudo
sudo python3 main.py
```

### Import Errors
```bash
# Reinstall packages
sudo pip3 install --force-reinstall -r requirements.txt
```

### Need to Stop the Game
Press `Ctrl+C` in the terminal

## Gameplay

1. **Startup**: Watch "TIC TAC TOE" spell out
2. **Red LED on**: Player X's turn
3. **Press button**: Place your symbol
4. **Blue LED on**: Player O's turn
5. **Win**: Rainbow animation + LED flash
6. **Draw**: Purple pulse animation
7. **Auto-reset**: New game starts automatically

## Next Steps

- See `README.md` for complete documentation
- Customize colors in `config.py`
- Adjust animations in `led_manager.py`
- Set up auto-start on boot (instructions in README.md)

## Support

Check the full `README.md` for detailed troubleshooting and hardware specifications.

---
**Have fun playing!** 🎮
