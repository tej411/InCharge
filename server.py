from flask import Flask, request, jsonify
import os
import socket

app = Flask(__name__)

# Define allowed scripts
ALLOWED_SCRIPTS = {
    "up": "up.py",
    "down": "down.py",
    "left": "left.py",
    "right": "right.py"
}

@app.route('/ping', methods=['GET'])
def ping():
    """Endpoint for discovery"""
    return "pong", 200

@app.route('/info', methods=['GET'])
def get_info():
    """Return server information"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return jsonify({
        "hostname": hostname,
        "ip": local_ip
    }), 200

@app.route('/run', methods=['POST'])
def run_script():
    data = request.json
    key = data.get("key")  # Key press from laptop
    
    if key in ALLOWED_SCRIPTS:
        script_name = ALLOWED_SCRIPTS[key]
        os.system(f'python3 {script_name}')  # Execute the script
        return f"Executed {script_name}", 200
    
    return "Invalid key", 400

if __name__ == '__main__':
    # Get and display the server's IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Server running at http://{local_ip}:5000")
    
    app.run(host='0.0.0.0', port=5000)  # Open to all devices on the network
