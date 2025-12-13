from flask import Flask, jsonify, request, render_template_string
import config

app = Flask(__name__)

robot_data = {"status": "idle", "battery": 85, "sensors": {"lidar": 120, "imu": [0, 0, 0]}, "command": "none"}


# Existing routes unchanged...
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(robot_data)


@app.route('/command', methods=['POST'])
def set_command():
    global robot_data
    data = request.json
    robot_data["command"] = data.get("command", "none")
    robot_data["status"] = "executing"
    return jsonify({"received": True})


@app.route('/telemetry', methods=['POST'])
def telemetry():
    global robot_data
    data = request.json
    robot_data.update(data)
    return jsonify({"ok": True})


# NEW: Simple browser upload form
@app.route('/', methods=['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        data = request.form.get('data')
        try:
            import json
            parsed = json.loads(data)
            robot_data.update(parsed)
            return render_template_string(HTML_FORM, message="✅ Data uploaded successfully!")
        except:
            return render_template_string(HTML_FORM, message="❌ Invalid JSON")

    return render_template_string(HTML_FORM, message="")


# NEW: Raw data view (for debugging)
@app.route('/data')
def view_data():
    return jsonify(robot_data)


HTML_FORM = '''
<!DOCTYPE html>
<html>
<body>
<h2>Robot Control Panel</h2>
<p>{{message}}</p>
<form method="POST">
<textarea name="data" rows="10" cols="50"
placeholder='{"command": "forward", "speed": 50, "target": "waypoint1"}'>{"command": "none"}</textarea><br>
<button type="submit">Upload to Robot</button>
</form>
<h3>Current Data:</h3>
<pre>{{data}}</pre>
<a href="/">Refresh</a>
</body>
</html>
'''

if __name__ == '__main__':
    print(f'Server with browser ui at http://www.{config.server['hostname']}:{config.server['port']}')
    app.run(host=config.server['internal_ip'], port=config.server['port'], debug=True)
