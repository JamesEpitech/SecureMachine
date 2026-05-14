# SecureMachine

SecureMachine is a Raspberry Pi project that detects movement or vibration using a tilt sensor and automatically records a video when activity is detected.

The project continuously monitors the sensor connected to the GPIO pins.
If movement is detected for a certain amount of time, the Raspberry Pi camera records a video and saves it locally.

It then sends this video to the given email address.

## Requirements

### Hardware
- Raspberry Pi
- Raspberry Pi Camera Module
- Tilt sensor

### Software
- Python3
- gpiozero
- rpicam-vid

Install required packages:

```bash
sudo apt update
sudo apt install python3-gpiozero rpicam-apps
```

## Project Structure
```
SecureMachine/
├── securemachine.py
└── Results/
```
Recorder videos are saved inside the `Results/` folder.

## How to use

### 1. Connect the Sensor
Connect the tilt sensor to:
- GPIO 17
- 3.3V
- GND

### 2. Enable the camera
Run:
```bash
sudo raspi-config
```

Enable the camera interface, then reboot the Raspberry Pi.

### 3. Run the script
```bash
python3 securemachine.py
```

## How it works
- The sensor is checked every 20ms
- Activity is analyzed over a 1 second window
- If enough movement is detected, a 10 second video is recorded

All of the values can changed in the code.
