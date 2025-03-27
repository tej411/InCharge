import requests
import keyboard
import socket
import time

# Function to discover Raspberry Pi on the network
def find_raspberry_pi():
    """Scan common ports on the local network to find the Raspberry Pi server"""
    print("Searching for Raspberry Pi server...")
    
    # Get local IP to determine network
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    
    # Get base network address
    base_ip = '.'.join(local_ip.split('.')[:-1]) + '.'
    
    # Try to connect to common ports on devices in the local network
    for i in range(1, 255):
        ip = f"{base_ip}{i}"
        try:
            response = requests.get(f"http://{ip}:5000/ping", timeout=0.1)
            if response.status_code == 200 and response.text == "pong":
                print(f"Found Raspberry Pi at {ip}")
                return ip
        except requests.exceptions.RequestException:
            continue
    
    return None

def send_command(key):
    """Send key press to Raspberry Pi"""
    try:
        response = requests.post(URL, json={"key": key})
        print(f"Sent '{key}', Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Try to find the Raspberry Pi automatically
RPI_IP = find_raspberry_pi()

# If automatic discovery fails, ask for manual input
if not RPI_IP:
    print("Could not find Raspberry Pi automatically.")
    RPI_IP = input("Please enter Raspberry Pi IP address manually: ")

URL = f"http://{RPI_IP}:5000/run"
print(f"Connected to Raspberry Pi at {RPI_IP}")

# Bind keys
KEYS_TO_WATCH = ["up", "down", "left", "right"]
for key in KEYS_TO_WATCH:
    keyboard.add_hotkey(key, send_command, args=(key,))

print("Listening for key presses... Press ESC to quit.")
keyboard.wait("esc")  # Keep script running until ESC is pressed