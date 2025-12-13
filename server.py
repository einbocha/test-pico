from flask import Flask, jsonify, request, render_template_string
import config  # Assuming config.server = {'hostname': '...', 'internal_ip': '...', 'port': 8000}

db = {}

HTML_FORM = '''
<!DOCTYPE html>
<html><body>
<h2>header ig</h2>
<p>{{message}}</p>
<form method="POST">
<textarea name="data" rows="10" cols="50"
placeholder='put here some JSON data'>{"test": 123}</textarea><br>
<button type="submit">to server</button>
</form>
<h3>Current Data:</h3>
<pre>{{data}}</pre>
<a href="/">Refresh</a>
</body></html>
'''

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])  # Handles both + JSON API
def upload_form():
    if request.method == 'POST':
        data = request.form.get('data')
        try:
            import json
            parsed = json.loads(data)
            db.update(parsed)
            return render_template_string(HTML_FORM, message="✅ Data uploaded successfully!", data=db)
        except:
            return render_template_string(HTML_FORM, message="❌ Invalid JSON", data=db)

    # GET: Browser form OR JSON API
    if request.headers.get('Accept') == 'application/json':
        return jsonify(db)
    return render_template_string(HTML_FORM, message="", data=db)

if __name__ == '__main__':
    print(f'Server with browser ui at http://{config.server["hostname"]}:{config.server["port"]}')
    app.run(host=config.server['internal_ip'], port=config.server['port'], debug=True)
