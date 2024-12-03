from flask import Flask, render_template, jsonify
import requests  # Make sure the `requests` library is installed

# Initialize the Flask application
app = Flask(__name__)

# URL of your JSON file hosted on GitHub or any other service
ROOMS_URL = "https://my-json-server.typicode.com/CyberEanid/ApiJSON/db"

# Function to load data from the hosted JSON file
def load_room_data():
    """Loads room and device data from the hosted JSON file."""
    try:
        response = requests.get(ROOMS_URL)
        response.raise_for_status()
        return response.json().get("rooms", [])
    except Exception as e:
        print(f"Error loading rooms: {e}")
        return []

# Load data once when the application starts
rooms = load_room_data()

# Route for the homepage
@app.route("/")
def index():
    """Homepage that lists all rooms."""
    return render_template("index.html", rooms=rooms)

# Route for a specific room's details
@app.route("/room/<room_name>")
def room_details(room_name):
    """Displays devices in a specific room."""
    room = next((r for r in rooms if r["name"].lower() == room_name.lower()), None)
    if room:
        return render_template("room_details.html", room=room)
    else:
        return render_template("error.html", message="Room not found"), 404

# Route for a specific device's details
@app.route("/device/<int:device_id>")
def device_details(device_id):
    """Displays details for a specific device."""
    for room in rooms:
        device = next((d for d in room["devices"] if d["id"] == device_id), None)
        if device:
            return render_template("device_details.html", device=device, room=room)
    return render_template("error.html", message="Device not found"), 404

# Run the application
if __name__ == "__main__":
    app.run(debug=True)

