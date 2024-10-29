from flask import Flask, request, jsonify

app = Flask(__name__)

# Example data structure for animation settings
animations = {
    "enabled": True,
    "animationClass": "wow fadeIn",
    "offset": 100,
    "mobile": True
}

# Endpoint to retrieve current animation settings
@app.route('/api/animation-settings', methods=['GET'])
def get_animation_settings():
    return jsonify(animations)

# Endpoint to update animation settings
@app.route('/api/animation-settings', methods=['POST'])
def update_animation_settings():
    data = request.json
    animations.update(data)  # Update the settings with provided data
    return jsonify({"message": "Settings updated", "animations": animations})

if __name__ == '__main__':
    app.run(port=5500)
