from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import langflow_api

load_dotenv()
LOCAL_LANGFLOW_API_KEY = os.getenv("LOCAL_LANGFLOW_API_KEY")

app = Flask(__name__, static_folder='static')

# Serve the static index.html   
@app.route('/', methods=['GET'])
def serve_index():
    return app.send_static_file('index.html')

# Handle POST requests from the front-end
@app.route('/', methods=['POST'])
def handle_post():
    data = request.get_json()
    user_message = data.get('userMessage', 'No message provided')

    response = langflow_api.run_flow(user_message, api_key=LOCAL_LANGFLOW_API_KEY)
    response = response["outputs"][0]["outputs"][0]["outputs"]["message"]["message"]["text"]

    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)