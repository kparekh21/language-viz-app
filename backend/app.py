from flask import Flask, request, jsonify
from flask_cors import CORS
from executor.python_executor import run_python_script
from executor.r_executor import run_r_script
import os

app = Flask(__name__)

# Allow all origins during development
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type"])

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()

    language = data.get('language')
    code = data.get('code')

    if not language or not code:
        return jsonify({'error': 'Missing language or code'}), 400

    if language == 'python':
        result = run_python_script(code)
    elif language == 'r':
        result = run_r_script(code)
    else:
        return jsonify({'error': 'Unsupported language'}), 400

    return jsonify(result)

if __name__ == '__main__':
    os.makedirs('temp_scripts', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5050)

