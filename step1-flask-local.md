# Run Project Locally

1. Create a new project in Pycharm

   ```bash
   pip install Flask
   ```

2. **Create the Flask application**:

   - Create a file named `app.py`.

3. **Write the Flask code**:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable to store the last posted JSON
last_json = None

@app.route('/data', methods=['POST'])
def post_json():
    global last_json
    # Get the JSON from the request
    last_json = request.get_json()
    return jsonify({"message": "JSON received"}), 200

@app.route('/data', methods=['GET'])
def get_json():
    if last_json is None:
        return jsonify({"message": "No JSON posted yet"}), 404
    return jsonify(last_json), 200

if __name__ == '__main__':
    app.run(debug=True)
```

3. **Run the Flask application**:

```bash
python app.py
```

4. **POST request**:

```bash
curl -X POST http://127.0.0.1:5000/data -H "Content-Type: application/json" -d '{"key": "value"}'
```

5. **GET request**:

```bash
curl http://127.0.0.1:5000/data
```

