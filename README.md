# Tic-Tac-Toe Game for Raspberry Pi Zero 2 W

A hardware-based Tic-Tac-Toe game using WS2812B LED matrices, featuring a stunning "TIC TAC TOE" startup animation and player-vs-player gameplay.

## Hardware Components

### Core Electronics
- **Raspberry Pi Zero 2 W** - Main controller
- **SN74AHCT125N** - Quad bus buffer for 3.3V to 5V logic level shifting
- **9× WS2812B 8×8 LED Matrix Panels** - Display grid
- **9× Momentary Push Buttons** - Input controls
- **2× LEDs** - Turn indicators (Red for Player X, Blue for Player O)
- **5V 10A Power Supply** - Powers the entire system
- **Inline Fuse Holder + 10A Blade Fuse** - Circuit protection
- **12V 10A Toggle Switch** - Main power switch

### Passive Components
- **9× 1000µF 16V Electrolytic Capacitors** - Power smoothing (one per LED matrix)
- **5× 330Ω Resistors** - Signal protection (3 for LED data lines, 2 for turn indicators)
- **Barrier Terminal Blocks** - Power distribution
- **18 AWG Wire, Heat Shrink** - Wiring and connections

### 3D Printed Enclosure
- PETG filament for strength and heat resistance
- 3×3 grid structure that snaps together like puzzle pieces

## GPIO Pin Configuration (BCM Numbering)

### Button Inputs (Pull-up, Active Low)
```
Panel 0 (Top-Left):     GPIO 17
Panel 1 (Top-Center):   GPIO 27
Panel 2 (Top-Right):    GPIO 22
Panel 3 (Mid-Left):     GPIO 23
Panel 4 (Mid-Center):   GPIO 24
Panel 5 (Mid-Right):    GPIO 25
Panel 6 (Bottom-Left):  GPIO 5
Panel 7 (Bottom-Center): GPIO 6
Panel 8 (Bottom-Right):  GPIO 13
```

### LED Matrix Data Lines (via SN74AHCT125N)
```
Row 0 (Panels 0, 1, 2): GPIO 12 (PWM0)
Row 1 (Panels 3, 4, 5): GPIO 18 (PWM0 alternate)
Row 2 (Panels 6, 7, 8): GPIO 19 (PWM1)
```

### Turn Indicator LEDs
```
Red LED (Player X):  GPIO 16
Blue LED (Player O): GPIO 20
```

## Software Installation

### 1. Update Raspberry Pi OS
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install System Dependencies
```bash
sudo apt install -y python3-pip python3-dev python3-setuptools
sudo apt install -y scons swig
```

### 3. Enable SPI (Required for NeoPixels)
```bash
sudo raspi-config
```
- Navigate to: **Interface Options** → **SPI** → **Enable**
- Reboot: `sudo reboot`

### 4. Install Python Dependencies
Navigate to the project directory:
```bash
cd tictactoe-raspi
```

Install required packages:
```bash
sudo pip3 install -r requirements.txt
```

### 5. Set Up Audio (Disable Audio to Free PWM Pins)
The WS2812B control uses PWM pins, which conflict with audio by default.

Edit `/boot/config.txt`:
```bash
sudo nano /boot/config.txt
```

Comment out or remove the line:
```
#dtparam=audio=on
```

Add at the end:
```
# Disable audio to free PWM pins for NeoPixels
dtoverlay=pwm,pin=12,func=4
dtoverlay=pwm-2chan,pin=18,func=2,pin2=19,func2=2
```

Save and reboot:
```bash
sudo reboot
```

## Running the Game

### Method 1: Direct Execution
Make the main script executable:
```bash
chmod +x main.py
```

Run with sudo (required for GPIO access):
```bash
sudo ./main.py
```

### Method 2: Python Command
```bash
sudo python3 main.py
```

### Run on Boot (Optional)
To auto-start the game on boot, add to `/etc/rc.local` before `exit 0`:
```bash
sudo nano /etc/rc.local
```

Add:
```bash
cd /home/pi/tictactoe-raspi
sudo python3 main.py &
```

## How to Play

1. **Power On**: The system displays "TIC TAC TOE" across all panels
2. **Game Start**: All panels clear, Red LED turns on (Player X's turn)
3. **Make a Move**: Press any button to place X or O on that panel
4. **Turn Indicator**: Red LED = Player X, Blue LED = Player O
5. **Win Condition**: Three in a row triggers a rainbow celebration animation
6. **Draw**: All panels filled with no winner shows purple pulse animation
7. **Auto-Reset**: Game automatically resets after completion

### Game Rules
- Player X (Red) always goes first
- Press a button to claim that panel
- Invalid moves (already occupied) are ignored
- First player to get 3 in a row (horizontal, vertical, or diagonal) wins
- If all 9 panels are filled with no winner, it's a draw

## Troubleshooting

### LEDs Don't Light Up
- Check 5V power supply is connected and switched on
- Verify capacitors are installed across 5V and GND for each matrix
- Confirm SN74AHCT125N buffer chip is properly wired
- Check GPIO pin connections match configuration
- Ensure SPI is enabled: `ls /dev/spidev*` should show devices

### Buttons Not Responding
- Verify buttons connect GPIO pins to GND when pressed
- Check internal pull-up resistors are enabled in code
- Test button continuity with multimeter
- Ensure GPIO pins aren't conflicting with other functions

### "Permission Denied" Error
- Always run with `sudo` for GPIO and PWM access
- Check file permissions: `chmod +x main.py`

### LEDs Flicker or Show Wrong Colors
- Add/check 1000µF capacitor on each matrix power line
- Verify 330Ω resistors on data lines
- Ensure power supply can deliver 10A
- Check for loose connections

### Import Errors
```bash
# Reinstall dependencies
sudo pip3 install --force-reinstall -r requirements.txt
```

### PWM/DMA Issues
```bash
# Check kernel modules
lsmod | grep pwm

# Verify device tree overlays
vcgencmd get_config int | grep dtoverlay
```

## Project Structure

```
tictactoe-raspi/
├── main.py              # Main entry point
├── game_controller.py   # Game logic and win detection
├── led_manager.py       # WS2812B LED matrix control
├── button_handler.py    # Button input with debouncing
├── turn_indicator.py    # Turn LED controller
├── patterns.py          # LED patterns (X, O, letters)
├── config.py           # GPIO pins and constants
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Technical Details

### Power Requirements
- Each WS2812B LED: ~60mA at full white brightness
- Total LEDs: 9 matrices × 64 LEDs = 576 LEDs
- Maximum theoretical draw: 576 × 60mA = 34.5A
- Actual usage (30% brightness, typical patterns): ~3-5A
- 10A power supply provides safety margin

### Data Signal Path
```
Raspberry Pi GPIO (3.3V) 
  → 330Ω Resistor 
  → SN74AHCT125N Buffer Input
  → SN74AHCT125N Buffer Output (5V)
  → WS2812B LED Matrix Data Input
```

### LED Matrix Wiring
- Each row of 3 matrices (192 LEDs) shares one data line
- Data flows: Matrix 0→1→2 (Row 0), 3→4→5 (Row 1), 6→7→8 (Row 2)
- Each matrix has 5V and GND connections with 1000µF capacitor

## Resources

- [Adafruit NeoPixel Guide](https://learn.adafruit.com/neopixels-on-raspberry-pi/overview)
- [WS2812B Datasheet](https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf)
- [SN74AHCT125N Datasheet](https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf)
- [RPi.GPIO Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)

## Credits

Hardware design and soldering skills: Thanks to Mache Creeger

## License

This project is for educational purposes. Feel free to modify and improve!
