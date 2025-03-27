import requests
import keyboard

RPI_IP = "172.20.10.5"  # Replace with your Raspberry Pi's actual IP
URL = f"http://{RPI_IP}:5000/run"

def send_command(key):
    """Send key press to Raspberry Pi"""
    try:
        response = requests.post(URL, json={"key": key})
        print(f"Sent '{key}', Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Bind keys
KEYS_TO_WATCH = ["up", "down", "left", "right"]

for key in KEYS_TO_WATCH:
    keyboard.add_hotkey(key, send_command, args=(key,))

print("Listening for key presses... Press ESC to quit.")
keyboard.wait("esc")  # Keep script running until ESC is pressed
