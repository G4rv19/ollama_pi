from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

def ollama(message):
    url   ='http://localhost:11434/api/generate'

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        "model": "tinyllama",
        "stream": False,
        "prompt": message
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data['response']
        return actual_response
    else:
        print("Error: ", response.status_code, response.text)
        return f"Error: {response.status_code} - {response.text}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/backend', methods=['POST'])
def process_message():
    message = request.get_json().get('message')
    try:
        reply = ollama(message)
    except Exception as e:
        print(f"Error in ollama function: {e}")
        return jsonify({'message': 'Error generating response'}), 500

    print(f"Received message: {message}")
    return jsonify({'message': reply})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')